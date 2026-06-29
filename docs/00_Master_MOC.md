# نقشه کل مستندات (Master Map of Content - MOC)
**هدف سند:** این فایل نقطه ورود (Entry Point) داکیومنت پروژه هستش.

پیش از باز کردن محیط توسعه (IDE) و نوشتن هر خط کد، مسیر مرتبط با وظیفه خود را از طریق این نقشه راه پیدا کرده و مطالعه کنید.

---

## راهنمای لایه‌های مستندات (Navigation Guide)

این پایگاه دانش به ۵ لایه مجزا تقسیم شده است. روی هر لینک کلیک کنید تا به سند مربوطه هدایت شوید:

### لایه صفر: استانداردهای تیم (Meta & Standards)
* [واژه‌نامه قطعی پروژه (Ubiquitous Language)](01_Meta_and_Standards/ubiquitous_language.md) - برای هم‌زبانی در نام‌گذاری متغیرها و کلاس‌ها.
* [استراتژی گیت و همکاری تیمی (Git Workflow)](01_Meta_and_Standards/git_workflow_team.md) - استراتژی برنچ‌ها، کامیت‌ها و نحوه ثبت Pull Request و مدیریت پروژه با گیت‌هاب.
* [مانیفست مهندسی و پروتکل‌ها (Development Protocols)](01_Meta_and_Standards/Development_Protocols/00_Protocols_MOC.md) - ورود به مانیفست مهندسی نرم‌افزار، اصول SOLID، ایزوله‌سازی و کدنویسی تدافعی.

###  لایه اول: محصول و برنامه‌ریزی (Product & Planning)
* [سند طراحی بازی (GDD)](02_Product_and_Planning/game_design_document.md) - توضیح کلی بازی که قصد داریم تولید کنیم و ویژگی های مد نظرمون.
* [ساختار شکست کار (WBS)](02_Product_and_Planning/work_breakdown_structure.md) - پخش وظایف توسعه بین اعضای تیم.
* [زمان‌بندی و مایل‌استون‌ها (Milestones)](02_Product_and_Planning/milestones_schedule.md) - زمان‌بندی توسعه بخش های مختلف، فازها (Sprints) و ددلاین‌ها از ۱۱ تیر تا ۲۰ تیر.

### لایه دوم: معماری کلان (Macro-Architecture)
* [معماری سورس‌کد و دایرکتوری‌ها](03_Architecture/src_directory_structure.md) - پوشه‌بندی پیشنهادی `src` و سورس دایرکتوری پروژه.
* [پشته تکنولوژی و ابزارها (Tech Stack)](03_Architecture/technology_stack.md) - لیست قطعی زبان‌ها، کتابخانه‌ها (مثل Pygame و SQLite)، ابزارهای مورد استفاده برای توسعه این پروژه.

### لایه سوم: معماری موتور بازی (Game Architecture)
* [گراف جریان فریم‌ها (Game Loop Pipeline)](04_Game_Architecture/game_loop_pipeline.md) - مراحل چهارگانه موتور بازی (Delta Time -> Events -> Update -> Render).
* [ماشین وضعیت (State Machine)](04_Game_Architecture/state_machine.md) - گراف وضعیت‌های برنامه (FSM) و نحوه انتقال بین منو، جریان بازی و صفحه نتایج.
* [گراف تزریق وابستگی (DI Graph)](04_Game_Architecture/dependency_injection_graph.md) - اینکه وابستگی‌ها چگونه در `bootstrap.py` ساخته و به هسته تزریق می‌شوند (IoC).

### لایه چهارم: معماری خرد و توسعه ماژول‌ها (Micro-Architecture)
وقتی وظیفه‌ای در WBS به شما محول می‌شود، شما به سندِ پوشه تحت مالکیت خود مراجعه کنید و براساس اون فایل ها و تسک های محول شده رو توسعه می‌دهید
* [راهنمای ماژول Main و مونتاژ](05_Modules_Documentation/module_main.md) - 
* [راهنمای ماژول Core (هسته)](05_Modules_Documentation/module_core.md) - راهنمای توسعه هسته اصلی، کلاک و توزیع رویدادها.
* [راهنمای ماژول Contracts (قراردادها)](05_Modules_Documentation/module_contracts.md) - راهنمای توسعه اینترفیس‌های انتزاعی سیستم (قوانین و پورت‌ها).
* [راهنمای ماژول Mechanics (مکانیک‌ها)](05_Modules_Documentation/module_mechanics.md) - راهنمای توسعه توابع ریاضی، فیزیک، تقاطع و سیستم کومبو.
* [راهنمای ماژول UI (رابط کاربری)](05_Modules_Documentation/module_ui.md) - راهنمای رندرینگ، مدیریت فونت‌ها و چیدمان HUD.
* [راهنمای ماژول Entities (موجودیت‌ها)](05_Modules_Documentation/module_entities.md) - راهنمای کپسوله‌سازی، ساختار داده‌های بازیکن، سیبل‌ها و آیتم‌ها.
* [راهنمای ماژول Database (پایگاه داده)](05_Modules_Documentation/module_database.md) - راهنمای اتصال ایمن به SQLite، نوشتن کوئری‌ها و استفاده از DTOها.
* [راهنمای ماژول Utils (ابزارها)](05_Modules_Documentation/module_utils.md) - راهنمای توسعه سیستم لاگر استاندارد و لودر فایل‌های استاتیک.

---

## قوانین

۱. **منبع حقیقت واحد (Single Source of Truth):** اگر در مورد نحوه پیاده‌سازی یک قابلیت شک داشتید یا اختلافی بین اعضای تیم به وجود آمد، حرف نهایی را اسناد موجود در این دایرکتوری می‌زنند.
۲. **مستندات زنده (Living Documentation):** اگر در حین توسعه متوجه شدید که نیاز به تغییر یک الگوریتم یا ساختار دارید، ابتدا باید سند مربوطه در این دایرکتوری را به‌روزرسانی کرده، در یک کامیت مجزا Push کنید و سپس کدهای خود را تغییر دهید.