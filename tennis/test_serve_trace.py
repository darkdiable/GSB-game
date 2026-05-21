import sys
sys.path.insert(0, '/Users/bilei/work/LargeModelAnnotation/GBS/260410/GSB-game/tennis')
from constants import *
from ball import Ball
from rules import TennisRules

print("=== 模拟完整发球流程（含违规检测）===")
print()

ball = Ball()
rules = TennisRules()

server_x = CENTER_MARK_X + 80
server_y = COURT_TOP + 30
target_x = CENTER_MARK_X - SERVICE_BOX_WIDTH // 2
target_y = NET_Y + 80
speed = BALL_SERVE_SPEED * 1.0

print(f"发球: NPC站右侧发球,目标({target_x}, {target_y})")
print(f"发球区: x∈[{CENTER_MARK_X - SERVICE_BOX_WIDTH}, {CENTER_MARK_X}], y∈[{NET_Y}, {SERVICE_LINE_BOTTOM}]")
print()

ball.serve(server_x, server_y, target_x, target_y, speed)

print("模拟球飞行和违规检测:")
print(f"{'帧':>4} | {'x':>7} | {'y':>7} | {'z':>7} | {'bounce':>6} | {'first_bc':>10} | 状态")
print("-" * 80)

violation_triggered = False

for frame in range(120):
    prev_bounce = ball.bounce_count
    prev_first_bc = ball.first_bounce_checked
    prev_z = ball.z
    prev_vz = ball.vz
    
    ball.update()
    
    status = ""
    
    if ball.bounce_count > prev_bounce:
        status += f"弹跳! {prev_bounce}->{ball.bounce_count}"
    
    if ball.first_bounce_checked and not prev_first_bc:
        status += " first_bc=True"
        serve_side = rules.get_serve_side()
        in_box = ball.is_in_service_box('npc', serve_side)
        status += f" 发球区:{in_box}"
        
        if not in_box:
            status += " ← 发球失误!"
            ball.in_play = False
            rules.fault()
            violation_triggered = True
            print(f"{frame:>4} | {ball.x:>7.1f} | {ball.y:>7.1f} | {ball.z:>7.1f} | {ball.bounce_count:>6} | {str(ball.first_bounce_checked):>10} | {status}")
            print(f"\n✗ 发球被判为失误!")
            print(f"  球的位置: x={ball.x:.1f}, y={ball.y:.1f}")
            print(f"  发球区: x∈[{CENTER_MARK_X - SERVICE_BOX_WIDTH}, {CENTER_MARK_X}], y∈[{NET_Y}, {SERVICE_LINE_BOTTOM}]")
            break
    
    if not violation_triggered and ball.z <= 0 and ball.vz <= 0.5 and ball.bounce_count >= 1 and not ball.first_bounce_checked:
        in_court = ball.is_in_court()
        status += f" 落地检查! z={ball.z:.1f}, vz={ball.vz:.1f}, bounce={ball.bounce_count}, 在场地:{in_court}"
        
        if not in_court:
            status += " ← 出界!"
            ball.in_play = False
            rules.out(ball.last_hit_by)
            violation_triggered = True
            print(f"{frame:>4} | {ball.x:>7.1f} | {ball.y:>7.1f} | {ball.z:>7.1f} | {ball.bounce_count:>6} | {str(ball.first_bounce_checked):>10} | {status}")
            print(f"\n✗ 球被判为出界!")
            print(f"  球的位置: x={ball.x:.1f}, y={ball.y:.1f}")
            print(f"  场地范围: x∈[{COURT_LEFT}, {COURT_RIGHT}], y∈[{COURT_TOP}, {COURT_BOTTOM}]")
            break
    
    if frame % 5 == 0 or status:
        print(f"{frame:>4} | {ball.x:>7.1f} | {ball.y:>7.1f} | {ball.z:>7.1f} | {ball.bounce_count:>6} | {str(ball.first_bounce_checked):>10} | {status}")
    
    if not ball.in_play:
        break
    
    if ball.first_bounce_checked:
        ball.first_bounce_checked = False

if not violation_triggered:
    print("\n✓ 发球未被判违规!")
