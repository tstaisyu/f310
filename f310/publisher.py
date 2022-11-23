import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import pygame
from pygame.locals import *

class PublisherNode(Node):
    # 初期化
    def __init__(self):
        super().__init__("publisher")
       
        # メッセージの準備
        self.msg = Int32()
        self.msg.data = 0
       
        # パブリッシャの準備
        self.pub = self.create_publisher(Int32, "direction", 0)

        # ジョイスティックの準備
        self.joystick = self.setupJoystick()
       
        # タイマーの準備
        self.tmr = self.create_timer(0.2, self.onTick)

    # ジョイスティックの準備
    def setupJoystick(self):
        # ジョイスティックの準備
        pygame.joystick.init()
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        # pygameの初期化
        pygame.init()

        # 画面の生成
        screen = pygame.display.set_mode((160, 160))
        screen.fill('white')
        pygame.display.update()
        return joystick        

    # 定期的に呼ばれる
    def onTick(self):
        # イベントの取得
        for e in pygame.event.get():
            # ジョイスティックのボタンの入力
            dx = self.joystick.get_axis(0)
            dy = self.joystick.get_axis(1)
            if e.type == pygame.locals.JOYAXISMOTION:
                if dy >= 0.5:
                    self.msg.data = 2
                elif dx < -0.5:
                    self.msg.data = 3
                elif dx > 0.5:
                    self.msg.data = 4
                elif dy < -0.5:
                    self.msg.data = 1
                else:
                    self.msg.data = 0

        # パブリッシュ
        self.get_logger().info("publish　: {0}".format(self.msg.data))
        self.pub.publish(self.msg)

def main(args=None):
    # プロセスの初期化
    rclpy.init(args=args)

    # ノードの生成
    node = PublisherNode()

    # ノードの処理をループ実行
    rclpy.spin(node)

    # ノードの破棄
    node.destroy_node()

    # プロセスの終了
    rclpy.shutdown()

if __name__ == "__main__":
    main()
