# ---- Stage 1: Build Stage ----
# این مرحله برای نصب وابستگی‌هاست تا ایمیج نهایی سبک‌تر باشه
FROM python:3.11-slim as builder

# ایجاد پوشه کاری
WORKDIR /app

# کپی کردن فایل نیازمندی‌ها
COPY requirements.txt .

# نصب وابستگی‌ها. --no-cache-dir حجم ایمیج رو کمتر می‌کنه
RUN pip install --no-cache-dir -r requirements.txt


# ---- Stage 2: Final Stage ----
# ساخت ایمیج نهایی که در پروداکشن اجرا میشه
FROM python:3.11-slim

# ایجاد پوشه کاری
WORKDIR /app

# کپی کردن کتابخانه‌های نصب شده از مرحله builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# *** مهم‌ترین تغییر: کپی کردن فایل‌های اجرایی (مثل gunicorn) از مرحله builder ***
COPY --from=builder /usr/local/bin /usr/local/bin

# کپی کردن کدهای اصلی برنامه
COPY ./app ./app

# کپی کردن پوشه داده‌ها
COPY ./data ./data

# باز کردن پورت 8000 برای دسترسی از بیرون کانتینر
EXPOSE 8000



# دستور پیش‌فرض برای اجرای برنامه
# این دستور توسط Start Command در Railway جایگزین (override) خواهد شد
# اما برای تست لوکال با Docker بسیار مفیده
CMD ["sh", "-c", "gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:${PORT:-8000}"]