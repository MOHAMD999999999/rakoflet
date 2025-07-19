[app]

# اسم التطبيق
title = QuizApp

# اسم الحزمة - استخدم اسم فريد (عادة بشكل نطاق معكوس)
package.name = quizapp
package.domain = org.example

# مسار ملفات المصدر (افتراضي هو مجلد العمل الحالي)
source.dir = .

# امتدادات الملفات التي سيتم تضمينها في التطبيق
source.include_exts = py,png,jpg,kv,json

# رقم إصدار التطبيق
version = 1.0.0

# المتطلبات - لغة بايثون ومكتبة كيفي
requirements = python3,kivy==2.1.0

# اتجاه الشاشة
orientation = portrait

# إعدادات أندرويد (يمكن تعديلها حسب الحاجة)
android.api = 33
android.minapi = 21
android.sdk = 24
android.ndk = 25b
android.arch = armeabi-v7a

# صلاحيات الأندرويد
android.permissions = INTERNET

# مستوى سجل الأحداث (2 = تحذيرات وأخطاء فقط)
log_level = 2

# تحذير عند التشغيل كروت (root)
warn_on_root = 1

# خيار الإيقاف المؤقت للصفحات 
fullscreen = 1
