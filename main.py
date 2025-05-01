from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import math

@register("clac_union_attack", "author", "合刀时间计算插件", "1.0.0", "repo_url")
class UnionAttackPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("合刀")
    async def union_attack(self, event: AstrMessageEvent):
        """
        计算合刀时间指令
        格式：/合刀 [boss血量] [A伤害] [B伤害]
        示例：/合刀 10000 3000 2000
        """
        try:
            # 分割消息参数
            args = event.message_str.split()[1:]
            
            # 参数校验
            if len(args) != 3:
                yield event.plain_result("❌ 参数错误！正确格式：/合刀 [boss血量] [A伤害] [B伤害]")
                return
                
            boss_hp, a_dmg, b_dmg = map(int, args)
            
            if b_dmg <= 0:
                yield event.plain_result("❌ B伤害必须大于0")
                return

            # 执行计算
            numerator = boss_hp - a_dmg
            if numerator <= 0:
                yield event.plain_result("⚠️ A伤害已经超过BOSS血量，无需补刀")
                return
                
            seconds = 100 - (numerator / b_dmg) * 90
            result = math.ceil(seconds)

            # 结果校验
            if result < 0:
                response = "❗ 计算结果异常：补刀时间小于0秒，请检查输入数值"
            else:
                response = (
                    f"🗡️ 合刀计算结果：\n"
                    f"BOSS剩余血量：{boss_hp}\n"
                    f"A刀伤害：{a_dmg}\n"
                    f"B刀需要伤害：{b_dmg}\n"
                    f"⏳ 预计补刀时间：{result}秒"
                )

            logger.info(f"合刀计算成功：{result}秒")
            yield event.plain_result(response)

        except ValueError:
            yield event.plain_result("❌ 参数必须为整数！")
        except Exception as e:
            logger.error(f"计算失败：{str(e)}")
            yield event.plain_result("⚠️ 计算时发生意外错误，请检查输入格式")

    async def terminate(self):
        """清理资源"""
        logger.info("合刀计算插件已卸载")
