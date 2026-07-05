# ساختار دایرکتوری و معماری نرم‌افزار (`src_directory_structure.md`)
**مسیر در پروژه:** `/src/`
**هدف:** ایجاد یک معماری کاملاً ماژولار (Highly Decoupled) بر پایه اصول SOLID، تزریق وابستگی (DI) و معماری پورت‌ها و آداپتورها (Ports and Adapters).

در این ساختار، هیچ ماژولی حق ندارد فراتر از مرزهای تعیین‌شده‌ی خود به فایل‌های دیگر وابستگی مستقیم (Tight Coupling) داشته باشد. ارتباطات صرفاً از طریق قراردادها (Contracts) صورت می‌پذیرد.

---

## 📂 نمای درختی پروژه (Tree View)

    src/
    ├── main.py
    ├── config/
    │   ├── settings.py
    │   ├── colors.py
    │   ├── keybinds.py
    │   └── thresholds.py
    ├── contracts/
    │   ├── i_database.py
    │   ├── i_renderable.py
    │   ├── i_collidable.py
    │   ├── i_audio_player.py
    │   └── i_state.py
    ├── core/
    │   ├── bootstrap.py
    │   ├── game_engine.py
    │   ├── state_manager.py
    │   ├── event_handler.py
    │   ├── input_mapper.py
    │   ├── auth_orchestrator.py
    │   └── delta_clock.py
    ├── entities/
    │   ├── base/
    │   │   └── game_object.py
    │   ├── player/
    │   │   ├── player_model.py
    │   │   └── crosshair.py
    │   ├── targets/
    │   │   ├── target_base.py
    │   │   └── standard_target.py
    │   └── items/
    │       ├── item_base.py
    │       ├── ammo_box.py
    │       ├── time_boost.py
    │       └── glitch_debuff.py
    ├── mechanics/
    │   ├── physics/
    │   │   ├── movement_system.py
    │   │   └── boundary_clamp.py
    │   ├── combat/
    │   │   ├── shooting_logic.py
    │   │   └── collision_detector.py
    │   ├── scoring/
    │   │   ├── math_formulas.py
    │   │   └── combo_tracker.py
    │   └── spawning/
    │       ├── coordinate_generator.py
    │       └── target_lifecycle.py
    ├── ui/
    │   ├── components/
    │   │   ├── text_renderer.py
    │   │   └── floating_number.py
    │   ├── hud/
    │   │   └── player_dashboard.py
    │   ├── vfx/
    │   │   ├── animation_manager.py 
    │   │   └── floating_text.py
    │   └── screens/
    │       ├── start_menu_screen.py
    │       ├── auth_screen.py
    │       └── leaderboard_screen.py
    ├── database/
    │   ├── connection_manager.py
    │   ├── models.py
    │   ├── dtos.py
    │   ├── queries.py
    │   └── sqlite_repository.py
    └── utils/
        ├── resource_loader.py
        ├── exception_logger.py
        └── audio_manager.py

---

## 📝 شرح وظایف لایه‌ها و رعایت پروتکل‌ها

### ۱. لایه پیکربندی (/src/config/)
این پوشه فقط شامل متغیرهای ثابت (Constants) است. هیچ‌گونه متد اجرایی یا منطق شرطی در این فایل‌ها وجود ندارد.

* settings.py: ابعاد پنجره نمایش (WIDTH, HEIGHT)، نرخ فریم (FPS)، مقادیر اولیه بازی (زمان ۱۰ ثانیه، تیر ۱۰ عدد) و حداکثر تعداد سیبل‌ها روی صفحه (۳ عدد).
* colors.py: تعریف کدهای RGB به صورت تاپل (مثلاً رنگ اختصاصی بازیکن ۱ و ۲، رنگ پس‌زمینه).
* keybinds.py: مپینگ کلیدهای کیبورد برای بازیکنان (جدا کردن کدهای Pygame مثل pygame.K_w از لاجیک هسته).
* thresholds.py: تنظیمات مربوط به بالانس بازی (مثلاً فواصل محاسبه امتیاز ۱ تا ۵، یا مدت زمان تأثیر آیتم Glitch).

### ۲. لایه قراردادها (`/src/contracts/`)
**نقش معماری:** قلب تپنده پنهان‌سازی اطلاعات (Information Hiding).
این پوشه فقط شامل کلاس‌های Abstract (در پایتون `abc.ABC` یا `typing.Protocol`) است. هیچ منطق اجرایی در اینجا وجود ندارد. سایر ماژول‌ها فقط این فایل‌ها را `import` می‌کنند تا بدانند با چه توابعی سروکار دارند، بدون اینکه از نحوه پیاده‌سازی آن‌ها مطلع باشند.

### ۳. لایه هسته و مونتاژ (`/src/core/`)
**نقش معماری:** مدیریت چرخه حیات و تزریق وابستگی (IoC/DI).
* **`bootstrap.py`:** این فایل بسیار حیاتی است. وظیفه آن این است که هنگام اجرای `main.py`، دیتابیس را روشن کند، تنظیمات را بخواند و آن‌ها را به عنوان پارامتر (تزریق) به کلاس `game_engine.py` پاس بدهد. انجین نباید خودش چیزی را Instantiate کند.
* **`game_engine.py`:** ارکستراتور اصلی که فازهای حلقه `while` را بر اساس قراردادها فراخوانی می‌کند.
* state_manager.py: مدیریت وضعیت‌های چهارگانه برنامه بر اساس [[state_machine.md]].
* event_handler.py: فقط مسئول پردازش pygame.event.get() و تبدیل آن‌ها به سیگنال‌های قابل فهم برای بقیه ماژول‌ها.
 * **`input_mapper.py`:**  ترجمه‌کننده کلیدهای خام کیبورد به فرمان‌های تفکیک‌شده برای بازیکن یک و دو (مثل `P1_SHOOT`). 
 * **`auth_orchestrator.py`:**  مدیر جریان احراز هویت یکپارچه که وظیفه تبادل داده بین فرم ورود و دیتابیس را دارد.
* delta_clock.py: مدیریت Delta Time و تبدیل تیک‌های Pygame به ثانیه‌های واقعی برای سیستم زمان‌سنجی بازیکنان.

### ۴. لایه موجودیت‌ها (`/src/entities/`)
**نقش معماری:** حفظ وضعیت (State Management) و رعایت اصل تغییرناپذیری در حد امکان.
این فایل‌ها فقط حاوی دیتای اشیاء بازی (مانند مختصات، جان، سرعت) هستند. آن‌ها نباید هیچ ارجاعی به کتابخانه `pygame` برای رسم کردن یا به `sqlite3` برای ذخیره شدن داشته باشند (رعایت دقیق Separation of Concerns).
پیاده‌سازی دقیق OOP. این فایل‌ها فقط داده‌ها (State) را نگه می‌دارند.

* base/game_object.py: کلاس بنیادین تمام اشیاء صفحه (شامل ویژگی‌های x, y و وضعیت زنده بودن).
* player/player_model.py: کپسوله‌سازی اطلاعات انتزاعی بازیکن (نام، رنگ، متدهای کسر تیر و زمان).
* player/crosshair.py: کپسوله‌سازی مختصات نشانگر و وضعیت is_visible (مخفی بودن قبل از شلیک اول).
* targets/target_base.py: والد اصلی تمام سیبل‌ها و پاورآپ‌ها.
* targets/standard_target.py: پیاده‌سازی سیبل‌های استاندارد.
* items/*: کلاسی برای هر آیتم، که متد apply_effect() آن به صورت پلی‌مورفیک (چندریختی) اورراید (Override) شده است.
### ۵. لایه مکانیک‌ها (`/src/mechanics/`)
**نقش معماری:** توابع خالص (Pure Functions) و بیزینس لاجیک ایزوله.
تمامی فایل‌های این پوشه (مانند `math_formulas.py`) باید تا حد امکان به شکل توابعی نوشته شوند که ورودی می‌گیرند و خروجی محاسبه‌شده را برمی‌گردانند، بدون اینکه متغیرهای Global را دستکاری کنند.
تمام محاسبات ریاضی و منطق فیزیک ایزوله شده در این پوشه است.

* physics/movement_system.py: دریافت ورودی کیبورد و جابجا کردن مختصات crosshair.py.
* physics/boundary_clamp.py: اطمینان از اینکه مختصات نشانگرها از WIDTH و HEIGHT خارج نمی‌شود.
* combat/shooting_logic.py: مدیریت منطق شلیک.
* combat/collision_detector.py: الگوریتم AABB یا بررسی تقاطع نقطه شلیک با شعاع سیبل‌ها.
* scoring/math_formulas.py: محاسبه خالص ریاضی با فرمول فیثاغورس.
* scoring/combo_tracker.py: نگه داشتن وضعیت (State) شلیک‌های متوالی و ریست کردن آن‌ها در صورت خطا.
* spawning/coordinate_generator.py: ایجاد مختصات تصادفی.
* spawning/target_lifecycle.py: کنترل چرخه حیات سیبل‌ها در بازی.

### ۶. لایه رابط کاربری (/src/ui/)
تمامی فراخوانی‌های pygame.draw یا رندر فونت منحصراً در این دایرکتوری انجام می‌شود.

* components/text_renderer.py: رندر متن‌ها در صفحه.
* components/floating_number.py: اعداد شناور در صفحه.
* hud/player_dashboard.py: رسم گرافیکی اطلاعات تیر، امتیاز و زمان بازیکن.
* vfx/animation_manager.py: پردازش و به‌روزرسانی انیمیشن‌های بصری با استفاده از زمان دلتا (dt).
* vfx/floating_text.py: نمایش اعداد شناور امتیاز که محو می‌شوند (Fade-out).
* screens/start_menu_screen.py: مدیریت فیلدهای متنی برای دریافت نام بازیکنان.
* screens/auth_screen.py: رسم فرم ورود داده برای نام کاربری و رمز عبور.
* screens/leaderboard_screen.py: رسم یک جدول گرافیکی از نفرات برتر.

### ۷. لایه پایگاه داده (/src/database/)
* connection_manager.py: مدیریت اتصال به فایل sqlite3 و اطمینان از بسته شدن ایمن کانکشن (Context Manager).
* models.py: تعریف ساختار جدولی دیتابیس (Data Classes).
* dtos.py: کلاس‌های انتقال داده.
* queries.py: فقط نگهدارنده رشته‌های خام SQL (دستورات SELECT و INSERT).
* sqlite_repository.py: متدهای سطح بالا (مثل save_match_results()) که توسط state_manager.py فراخوانی می‌شوند.
  
### ۸. لایه ابزارها (/src/utils/)
* resource_loader.py: لود کردن ایمن تصاویر و صداها از پوشه assets/.
* exception_logger.py: سیستم ثبت لاگ برای دیباگ کردن خطاها.
* audio_manager.py: پیاده‌ساز قرارداد صوتی با قابلیت خواندن فایل‌های صوتی و تخصیص کانال‌های همزمان پخش برای جلوگیری از تداخل.