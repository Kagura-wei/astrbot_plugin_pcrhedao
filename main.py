from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import math

@register("pcrhedao", "作者名", "PCR合刀计算插件", "1.1.0", "https://example.com")
class PcrHeDaoPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        logger.info("合刀插件已加载")

    @filter.command("合刀")
    async def calculate_union_attack(self, event: AstrMessageEvent):
        """计算合刀时间指令
        格式：/合刀 [boss血量] [A伤害] [B伤害]
        示例：/合刀 15000 8000 5000
        """
        try:
            # 分割消息参数
            cmd_args = event.message_str.split()
            
            # 参数完整性校验
            if len(cmd_args) < 4:
                yield event.plain_result("⚠️ 参数不足！正确格式：/合刀 [boss血量] [A伤害] [B伤害]")
                return
                
            _, boss_hp_str, a_dmg_str, b_dmg_str = cmd_args[:4]

            # 类型转换校验
            try:
                boss_hp = int(boss_hp_str)
                a_dmg = int(a_dmg_str)
                b_dmg = int(b_dmg_str)
            except ValueError:
                yield event.plain_result("❌ 参数必须为整数数字！")
                return

            # 逻辑校验
            if b_dmg <= 0:
                yield event.plain_result("❗ B刀伤害必须大于0")
                return

            if a_dmg >= boss_hp:
                yield event.plain_result("💡 A刀伤害已超过BOSS血量，无需补刀")
                return

            # 核心计算逻辑
            remaining_hp = boss_hp - a_dmg
            time_ratio = remaining_hp / b_dmg
            seconds = 100 - time_ratio * 90
            result = math.ceil(seconds)

            # 结果有效性判断
            if result < 0:
                response = "⚠️ 计算结果异常：补刀时间为负数，请检查输入数值"
            elif result > 90:
                response = "⏱️ 补刀时间超过90秒，建议直接出刀"
            else:
                response = (
                    "🗡️ 合刀计算结果：\n"
                    f"• BOSS剩余血量：{boss_hp}\n"
                    f"• A刀伤害：{a_dmg}\n"
                    f"• B刀需求伤害：{b_dmg}\n"
                    f"⏳ 预计补刀时间：{result}秒"
                )

            logger.debug(f"用户 {event.get_sender_name()} 计算结果：{result}秒")
            yield event.plain_result(response)

        except Exception as e:
            logger.error(f"计算失败：{str(e)}", exc_info=True)
            yield event.plain_result("🌀 计算时发生意外错误，请稍后重试")

    async def terminate(self):
        """插件卸载时的清理操作"""
        logger.info("合刀插件已安全卸载")
        await super().terminate()
