from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import math

@register("knife_calculator", "刀伤计算器作者", "合刀时间计算插件", "1.0.0", "https://github.com/your_repo")
class KnifeCalculator(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("合刀")
    async def calculate_knife(self, event: AstrMessageEvent):
        '''合刀时间计算器
        格式：合刀 [BOSS血量] [A伤害] [B伤害]
        示例：合刀 1000000 500000 300000'''
        
        try:
            # 解析消息参数（网页1、2、4提到的消息处理方式）
            params = event.message_str.split()[1:]  # 去除指令头
            if len(params) != 3:
                raise ValueError("参数数量错误")
                
            boss_hp, a_dmg, b_dmg = map(int, params)  # 转换为整数（网页6、7、8提到的数值处理）
            
            # 公式计算（用户提供的公式）
            time_seconds = 100 - ((boss_hp - a_dmg) / b_dmg) * 90
            result = math.ceil(time_seconds)  # 向上取整（网页6、7、8重点说明）
            
            # 构造返回消息（网页1、2、4的回复格式参考）
            reply = (
                f"⚔️ 合刀计算结果：\n"
                f"BOSS剩余血量：{boss_hp - a_dmg}\n"
                f"理论补时秒数：{time_seconds:.2f}秒\n"
                f"向上取整结果：{result}秒"
            )
            
            logger.info(f"成功计算合刀：{params} -> {result}s")
            
        except ValueError as e:
            logger.warning(f"参数错误：{str(e)}")
            reply = "❌ 参数错误！正确格式：合刀 [BOSS血量] [A伤害] [B伤害]\n示例：合刀 1000000 500000 300000"
        except ZeroDivisionError:
            logger.error("除零错误：B伤害不能为0")
            reply = "❌ 计算错误：B伤害值不能为0"
        except Exception as e:
            logger.error(f"未知错误：{str(e)}")
            reply = "⚠️ 系统异常，请检查输入格式"
        
        yield event.plain_result(reply)

    async def terminate(self):
        '''插件卸载时的清理操作'''
        logger.info("合刀计算插件已安全卸载")
