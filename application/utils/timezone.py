from datetime import timezone
import pytz


china_tz = pytz.timezone('Asia/Shanghai')
now = timezone.localtime(timezone.now(), china_tz)