from django.db import models
from django.utils.translation import gettext_lazy as _


class Position(models.TextChoices):
    CHAIRPERSON = 'chairperson', _("Chủ tịch")
    GENERAL_MANAGER = 'general_manager', _("Tổng giám đốc")
    MANAGING_DIRECTOR = 'manager_director', _("Phó TGĐ/Giám đốc KD/ GĐ khối")
    REGIONAL_DIRECTOR = 'regional_director', _("Giám đốc khu vực/Bá tước")
    MANAGER = 'manager', _("Giám đốc chuyên môn/Trưởng phòng")
    LEADER = 'leader', _("Trưởng bộ phận/Trưởng nhóm")
    ASSISTANT = 'assistant', _("Trợ lý")
    SECRETARY = 'secretary', _("Thư ký")
    ACCOUNTANT = 'accountant', _("Kế toán")
    COORDINATOR = 'coordinator', _("Điều phối viên")
    EXPERT_HOME = 'expert_home', _("Chuyên viên Đầu chủ")
    EXPERT = 'expert', _("Chuyên viên")
    INTERNS = 'interns', _("Học viên")


class Title(models.TextChoices):
    SUPERMAN = 'superman', _("Siêu nhân")
    PROFESSOR = 'professor', _("Giáo sư")
    EXPERT = 'expert', _("Chuyên gia")
    MASTER = 'master', _("Cao thủ")
    COMPETENTLY = 'competently', _("Thạo nghề")
    PROBATIONARY = 'probationary', _("Tập sự")
    ROOKIE = 'rookie',_("Tân binh")


class Workplace(models.TextChoices):
    TGNP = 'tgnp', _("Thế Giới Nhà Phố Việt Nam")
    THIENKHOI = 'thienkhoi', _("Thiên Khôi")
    NHAPHO = 'nhapho', _("Nhà Phố Việt Nam")
    KIMLAND = 'kimland', _("Kim Land")
    TUAN123 = 'tuan123',_("Tuấn 123")
    PHOXANH = 'phoxanh', _("Phố Xanh")
    SUMO = 'sumo', _("Sumo")
    VUDA = 'vuda', _("Vuda Home")
    OTHER = 'other', _("Đơn vị khác")


class Status(models.TextChoices):
    COOPERATING = 'cooperating', _("Đang hợp tác")
    PAUSE_COOPERATING = 'pause_cooperating', _("Tạm dừng")
    STOP_COOPERATING = 'stop_cooperating', _("Ngừng hợp tác")
