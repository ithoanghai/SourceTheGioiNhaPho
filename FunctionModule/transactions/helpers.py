import sys
import traceback

from FunctionModule.customers.choices import CustomerType
from FunctionModule.realtors.choices import Position, Title
from FunctionModule.transactions.models import TransTypeInit


def get_short_title_from_trans_type(trans_type: str):
    if trans_type == TransTypeInit.CONTACT:
        return 'Liên hệ'
    elif trans_type == TransTypeInit.VIEW:
        return 'Liên hệ xem BĐS'
    elif trans_type == TransTypeInit.ORDER:
        return 'Đặt hàng'
    elif trans_type == TransTypeInit.BUY:
        return 'Mua BĐS'
    elif trans_type == TransTypeInit.SELL:
        return 'Bán BĐS'
    elif trans_type == TransTypeInit.RENT:
        return 'Thuê BĐS'
    elif trans_type == TransTypeInit.LEASE:
        return 'Cho thuê BĐS'
    elif trans_type == TransTypeInit.INTRO_ESTATE:
        return 'Giới thiệu BĐS'
    elif trans_type == TransTypeInit.INTRO_CUSTO:
        return 'Giới thiệu khách'


def get_short_title_from_customer_type(customer_type: str):
    if customer_type == CustomerType.BUY_LIVE:
        return 'Mua để ở'
    elif customer_type == CustomerType.KEEP_MONEY:
        return 'Giữ tiền'
    elif customer_type == CustomerType.INVESTMENT_CONSTRUCTION:
        return 'Đầu tư xây bán'
    elif customer_type == CustomerType.SURF_INVESTMENT:
        return 'Đầu tư lướt sóng'


def get_short_title_from_position_type(position_type: str):
    if position_type == Position.CHAIRPERSON:
        return 'Chủ tịch'
    elif position_type == Position.GENERAL_MANAGER:
        return 'Tổng giám đốc'
    elif position_type == Position.MANAGING_DIRECTOR:
        return 'Phó TGĐ/Giám đốc khối'
    elif position_type == Position.REGIONAL_DIRECTOR:
        return 'Giám đốc khu vực/Bá tước'
    elif position_type == Position.MANAGER:
        return 'Giám đốc chuyên môn/Trưởng phòng'
    elif position_type == Position.LEADER:
        return 'Trưởng bộ phận/Trưởng nhóm'
    elif position_type == Position.ASSISTANT:
        return 'Trợ lý'
    elif position_type == Position.ACCOUNTANT:
        return 'Kế toán'
    elif position_type == Position.COORDINATOR:
        return 'Điều phối viên'
    elif position_type == Position.EXPERT_HOME:
        return 'Chuyên viên Đầu chủ'
    elif position_type == Position.EXPERT:
        return 'Chuyên viên'
    elif position_type == Position.INTERNS:
        return 'Học viên'


def get_short_title_type(title_type: str):
    if title_type == Title.SUPERMAN:
        return 'Siêu nhân'
    elif title_type == Title.PROFESSOR:
        return 'Giáo sư'
    elif title_type == Title.EXPERT:
        return 'Chuyên gia'
    elif title_type == Title.MASTER:
        return 'Cao thủ'
    elif title_type == Title.COMPETENTLY:
        return 'Thạo nghề'
    elif title_type == Title.PROBATIONARY:
        return 'Tập sự'
    elif title_type == Title.ROOKIE:
        return 'Tân binh'