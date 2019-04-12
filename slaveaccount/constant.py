# encoding: UTF-8
import datetime as dt

# from slaveaccount.ctp import defineDict
from slaveaccount.ctp import *

# 默认空值
EMPTY_STRING = ''
EMPTY_UNICODE = ''
EMPTY_INT = 0
EMPTY_FLOAT = 0.0

# 方向常量
DIRECTION_NONE = '无方向'
DIRECTION_LONG = '多'
DIRECTION_SHORT = '空'
DIRECTION_UNKNOWN = '未知'
DIRECTION_NET = '净'
DIRECTION_SELL = '卖出'              # IB接口
DIRECTION_COVEREDSHORT = '备兑空'    # 证券期权

# 开平常量
OFFSET_NONE = '无开平'
OFFSET_OPEN = '开仓'
OFFSET_CLOSE = '平仓'
OFFSET_CLOSETODAY = '平今'
OFFSET_CLOSEYESTERDAY = '平昨'
OFFSET_UNKNOWN = '未知'

# 状态常量
STATUS_NOTTRADED = '未成交'
STATUS_PARTTRADED = '部分成交'
STATUS_ALLTRADED = '全部成交'
STATUS_CANCELLED = '已撤销'
STATUS_REJECTED = '拒单'
STATUS_UNKNOWN = '未知'

# 合约类型常量
PRODUCT_EQUITY = '股票'
PRODUCT_FUTURES = '期货'
PRODUCT_OPTION = '期权'
PRODUCT_INDEX = '指数'
PRODUCT_COMBINATION = '组合'
PRODUCT_FOREX = '外汇'
PRODUCT_UNKNOWN = '未知'
PRODUCT_SPOT = '现货'
PRODUCT_DEFER = '延期'
PRODUCT_ETF = 'ETF'
PRODUCT_WARRANT = '权证'
PRODUCT_BOND = '债券'
PRODUCT_NONE = ''

# 价格类型常量
PRICETYPE_LIMITPRICE = '限价'
PRICETYPE_MARKETPRICE = '市价'
PRICETYPE_FAK = 'FAK'
PRICETYPE_FOK = 'FOK'

# 期权类型
OPTION_CALL = '看涨期权'
OPTION_PUT = '看跌期权'

# 交易所类型
EXCHANGE_SSE = 'SSE'       # 上交所
EXCHANGE_SZSE = 'SZSE'     # 深交所
EXCHANGE_CFFEX = 'CFFEX'   # 中金所
EXCHANGE_SHFE = 'SHFE'     # 上期所
EXCHANGE_CZCE = 'CZCE'     # 郑商所
EXCHANGE_DCE = 'DCE'       # 大商所
EXCHANGE_SGE = 'SGE'       # 上金所
EXCHANGE_INE = 'INE'       # 国际能源交易中心
EXCHANGE_UNKNOWN = 'UNKNOWN'# 未知交易所
EXCHANGE_NONE = ''          # 空交易所
EXCHANGE_HKEX = 'HKEX'      # 港交所
EXCHANGE_HKFE = 'HKFE'      # 香港期货交易所


EXCHANGE_SMART = 'SMART'       # IB智能路由（股票、期权）
EXCHANGE_NYMEX = 'NYMEX'       # IB 期货
EXCHANGE_GLOBEX = 'GLOBEX'     # CME电子交易平台
EXCHANGE_IDEALPRO = 'IDEALPRO' # IB外汇ECN

EXCHANGE_CME = 'CME'           # CME交易所
EXCHANGE_ICE = 'ICE'           # ICE交易所
EXCHANGE_LME = 'LME'           # LME交易所

EXCHANGE_OANDA = 'OANDA'       # OANDA外汇做市商
EXCHANGE_FXCM = 'FXCM'         # FXCM外汇做市商

EXCHANGE_OKCOIN = 'OKCOIN'       # OKCOIN比特币交易所
EXCHANGE_HUOBI = 'HUOBI'         # 火币比特币交易所
EXCHANGE_LBANK = 'LBANK'         # LBANK比特币交易所
EXCHANGE_KORBIT = 'KORBIT'	 # KORBIT韩国交易所
EXCHANGE_ZB = 'ZB'		 # 比特币中国比特币交易所
EXCHANGE_OKEX = 'OKEX'		 # OKEX比特币交易所
EXCHANGE_ZAIF = "ZAIF"		 # ZAIF日本比特币交易所
EXCHANGE_COINCHECK = "COINCHECK" # COINCHECK日本比特币交易所

# 货币类型
CURRENCY_USD = 'USD'            # 美元
CURRENCY_CNY = 'CNY'            # 人民币
CURRENCY_HKD = 'HKD'            # 港币
CURRENCY_UNKNOWN = 'UNKNOWN'    # 未知货币
CURRENCY_NONE = ''              # 空货币

# 数据库
LOG_DB_NAME = 'VnTrader_Log_Db'

# 接口类型
GATEWAYTYPE_EQUITY = 'equity'                   # 股票、ETF、债券
GATEWAYTYPE_FUTURES = 'futures'                 # 期货、期权、贵金属
GATEWAYTYPE_INTERNATIONAL = 'international'     # 外盘
GATEWAYTYPE_BTC = 'btc'                         # 比特币
GATEWAYTYPE_DATA = 'data'                       # 数据（非交易）


LOADING_ERROR = '读取连接配置出错，请检查'
CONFIG_KEY_MISSING = '连接配置缺少字段，请检查'

DATA_SERVER_CONNECTED = '行情服务器连接成功'
DATA_SERVER_DISCONNECTED = '行情服务器连接断开'
DATA_SERVER_LOGIN = '行情服务器登录完成'
DATA_SERVER_LOGOUT = '行情服务器登出完成'

TRADING_SERVER_CONNECTED = '交易服务器连接成功'
TRADING_SERVER_DISCONNECTED = '交易服务器连接断开'
TRADING_SERVER_AUTHENTICATED = '交易服务器验证成功'
TRADING_SERVER_LOGIN = '交易服务器登录完成'
TRADING_SERVER_LOGOUT = '交易服务器登出完成'

SETTLEMENT_INFO_CONFIRMED = '结算信息确认完成'
CONTRACT_DATA_RECEIVED = '交易合约信息获取完成'

# 以下为一些VT类型和CTP类型的映射字典
# 价格类型映射
priceTypeMap = {}
priceTypeMap[PRICETYPE_LIMITPRICE] = THOST_FTDC_OPT_LimitPrice
priceTypeMap[PRICETYPE_MARKETPRICE] = THOST_FTDC_OPT_AnyPrice
priceTypeMapReverse = {v: k for k, v in list(priceTypeMap.items())}

# 方向类型映射
directionMap = {}
directionMap[DIRECTION_LONG] = THOST_FTDC_D_Buy
directionMap[DIRECTION_SHORT] = THOST_FTDC_D_Sell
directionMapReverse = {v: k for k, v in list(directionMap.items())}

# 开平类型映射
offsetMap = {}
offsetMap[OFFSET_OPEN] = THOST_FTDC_OF_Open
offsetMap[OFFSET_CLOSE] = THOST_FTDC_OF_Close
offsetMap[OFFSET_CLOSETODAY] = THOST_FTDC_OF_CloseToday
offsetMap[OFFSET_CLOSEYESTERDAY] = THOST_FTDC_OF_CloseYesterday
offsetMapReverse = {v: k for k, v in list(offsetMap.items())}

# 交易所类型映射
exchangeMap = {}
exchangeMap[EXCHANGE_CFFEX] = 'CFFEX'
exchangeMap[EXCHANGE_SHFE] = 'SHFE'
exchangeMap[EXCHANGE_CZCE] = 'CZCE'
exchangeMap[EXCHANGE_DCE] = 'DCE'
exchangeMap[EXCHANGE_SSE] = 'SSE'
exchangeMap[EXCHANGE_SZSE] = 'SZSE'
exchangeMap[EXCHANGE_INE] = 'INE'
exchangeMap[EXCHANGE_UNKNOWN] = ''
exchangeMapReverse = {v: k for k, v in list(exchangeMap.items())}

# 持仓类型映射
posiDirectionMap = {}
posiDirectionMap[DIRECTION_NET] = THOST_FTDC_PD_Net
posiDirectionMap[DIRECTION_LONG] = THOST_FTDC_PD_Long
posiDirectionMap[DIRECTION_SHORT] = THOST_FTDC_PD_Short
posiDirectionMapReverse = {v: k for k, v in list(posiDirectionMap.items())}

# 产品类型映射
productClassMap = {}
productClassMap[PRODUCT_FUTURES] = THOST_FTDC_PC_Futures
productClassMap[PRODUCT_OPTION] = THOST_FTDC_PC_Options
productClassMap[PRODUCT_COMBINATION] = THOST_FTDC_PC_Combination
productClassMapReverse = {v: k for k, v in list(productClassMap.items())}
# productClassMapReverse[THOST_FTDC_PC_ETFOption] = PRODUCT_OPTION
# productClassMapReverse[THOST_FTDC_PC_Stock] = PRODUCT_EQUITY

# 委托状态映射
statusMap = {}
statusMap[STATUS_ALLTRADED] = THOST_FTDC_OST_AllTraded
statusMap[STATUS_PARTTRADED] = THOST_FTDC_OST_PartTradedQueueing
statusMap[STATUS_NOTTRADED] = THOST_FTDC_OST_NoTradeQueueing
statusMap[STATUS_CANCELLED] = THOST_FTDC_OST_Canceled
statusMapReverse = {v: k for k, v in list(statusMap.items())}

# 全局字典, key:symbol, value:exchange
symbolExchangeDict = {}

# 夜盘交易时间段分隔判断
NIGHT_TRADING = dt.datetime(1900, 1, 1, 20).time()

CONTRACT_DATA_RECEIVED = '交易合约信息获取完成'