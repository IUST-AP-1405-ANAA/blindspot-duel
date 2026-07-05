# گراف جریان فریم‌ها و معماری حلقه اصلی (Game Loop Pipeline)
**هدف:** تشریح چرخه حیات بی‌نهایت (Infinite Loop) موتور بازی، تعریف دقیق فازهای اجرایی در هر فریم، و تضمین رعایت اصل جداسازی دغدغه‌ها (SoC) در جریان اجرای برنامه.

این سند به عنوان نقشه راه برای توسعه فایل `game_engine.py` عمل می‌کند. 

---

## ۱. فلسفه حلقه اصلی (The Heartbeat of the Engine)

در معماری ما، موتور بازی (Game Engine) یک «ارکستراتور» است، نه یک محاسبه‌گر. حلقه اصلی بازی (Game Loop) به هیچ‌وجه نباید درگیر محاسبات پیچیده شود؛ بلکه تنها وظیفه دارد فازهای مختلف را به ترتیب، در هر فریم (Frame) فراخوانی کرده و وابستگی‌ها را به لایه‌های زیرین پاس بدهد. 

---

## ۲. مراحل اجرایی پایپ‌لاین (The 4-Phase Pipeline)

هر فریم از بازی دقیقاً به ۴ فاز ایزوله و متوالی تقسیم می‌شود. 

### ⏱️ فاز صفر: محاسبه زمان دلتا (Delta Time / dt)
پیش از شروع منطق هر فریم، زمان سپری‌شده از فریم قبلی (بر حسب ثانیه) محاسبه می‌شود تا بازی در سیستم‌های مختلف سرعت یکسانی داشته باشد.

### 📥 فاز اول: پردازش رویدادها (Event Polling & Input Mapping)
در این فاز، موتور بازی تمام ورودی‌های سخت‌افزاری را دریافت می‌کند. کلاس `EventHandler` رویدادها را گرفته و به `InputMapper` می‌فرستد تا به فرمان‌های ایزوله ترجمه شوند.

### 🧠 فاز دوم: به‌روزرسانی وضعیت (State Update)
مغز بازی در این فاز فعال می‌شود. در این مرحله هیچ‌چیزی روی صفحه رسم نمی‌شود.
موتور بازی فقط متد `update` از `state_manager` را با زمان دلتا و فرمان‌ها صدا می‌زند. منطق اصلی براساس وضعیت کنونی (مثل بازی یا منو) درون متدهای آپدیت کلاس‌های وضعیت انجام می‌شود.

### 🎨 فاز سوم: رندر و نمایش (Render Pipeline)
موتور بازی دستور رسم را صادر می‌کند:
1. **پاک‌سازی (Clear):** کل صفحه پاک می‌شود.
2. **رسم وضعیت (Render State):** متد `render` از `state_manager` صدا زده می‌شود تا وضعیت فعلی گرافیک خودش را رسم کند.
3. **تعویض بافر (Buffer Flip):** صفحه جدید نمایش داده می‌شود.

---

## ۳. شبه‌کد ساختاری حلقه (Pipeline Pseudo-code)

ساختار انتزاعی حلقه اصلی در هسته سیستم (`run` در `game_engine.py`) دقیقاً از الگوی زیر پیروی می‌کند:

```Python
def run(self) -> None:
    """The main while loop (events -> update -> render)."""
    while self.is_running and self.state_manager.is_running:
        # Phase 0: Delta Time
        dt = self.clock.tick()
        
        # Phase 1: Event Polling
        events = self.event_handler.poll_events()
        if not self.event_handler.is_window_open:
            self.is_running = False
            break
            
        # Input Mapping
        commands = self.input_mapper.map_inputs(events)
        
        # Phase 2: Update logic based on state
        self.state_manager.update(dt, commands)
        
        # Update animations
        self.animation_manager.update(dt)
        
        # Phase 3: Render
        self.renderer.clear_screen(BG_COLOR)
        self.state_manager.render(self.renderer)
        
        # Draw float text VFX over state renders
        self.vfx_system.render(self.renderer)
        
        self.renderer.flip_buffer()
```

## ۴. خطوط قرمز معماری در حلقه اصلی (Strict Constraints)

1. **عدم استفاده از شرط برای وضعیت در موتور بازی:** موتور بازی فقط یک هماهنگ کننده است. از نوشتن شرط‌های `if/else` برای اجرای منطق وضعیت‌های مختلف به شدت پرهیز کنید.
2. **ممنوعیت Mutation در فاز رندر:** فاز رندر باید یک عملیات صرفاً خواندنی (Read-only) باشد.