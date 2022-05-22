import sys
import traceback

from FunctionModule.customers.choices import CustomerType
from FunctionModule.listings.choices import Position, Title
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
        return 'Giám đốc điều hành'
    elif position_type == Position.BUSINESS_MANAGER:
        return 'Giám đốc kinh doanh'
    elif position_type == Position.REGIONAL_DIRECTOR:
        return 'Giám đốc khu vực'
    elif position_type == Position.TECHNICAL_DIRECTOR:
        return 'Giám đốc kỹ thuật'
    elif position_type == Position.MANAGER:
        return 'Quản lý/Trưởng phòng'
    elif position_type == Position.ASSISTANT:
        return 'Trợ lý'
    elif position_type == Position.ACCOUNTANT:
        return 'Kế toán'
    elif position_type == Position.COORDINATOR:
        return 'Điều phối viên'
    elif position_type == Position.EXPERT:
        return 'Chuyên viên'
    elif position_type == Position.INTERNS:
        return 'Học viên'
    elif position_type == Position.USER:
        return 'Người dùng thông thường'


def get_short_title_type(title_type: str):
    if title_type == Title.PROFESSOR:
        return 'Giáo sư'
    elif title_type == Title.EXPERT:
        return 'Chuyên gia'
    elif title_type == Title.MASTER:
        return 'Cao thủ'
    elif title_type == Title.PROBATIONARY:
        return 'Tập sự'
    elif title_type == Title.ROOKIE:
        return 'Tân binh'