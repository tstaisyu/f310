import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial
import time

class SubscriberNode(Node):
    # 初期化
    def __init__(self):
        super().__init__("subscriber")

        # シリアル通信のオープン
        self.ser = serial.Serial(
            port='/dev/tty0', # デバイス名 
            baudrate=115200, # ポート番号
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        time.sleep(2)

        # サブスクライブの準備
        self.direction = 0
        self.create_subscription(Int32, "direction", self.onSubscribed, 10)

    # サブスクライブ時に呼ばれる
    def onSubscribed(self, msg):
        self.get_logger().info("subscribe : {0}".format(msg.data))
        if self.direction != msg.data:
            self.direction = msg.data

            # スキルの実行
            if self.direction == 0:
                self.ser.write(str.encode('kbalance\n'))
            elif self.direction == 1:
                self.ser.write(str.encode('kwkF\n'))
            elif self.direction == 2:
                self.ser.write(str.encode('kbk\n'))
            elif self.direction == 3:
                self.ser.write(str.encode('kwkL\n'))
            elif self.direction == 4:
                self.ser.write(str.encode('kwkR\n'))
            time.sleep(0.2)

def main(args=None):
    # プロセスの初期化
    rclpy.init(args=args)

    # ノードの生成
    node = SubscriberNode()

    # ノードの処理をループ実行
    rclpy.spin(node)

    # ノードの破棄
    node.destroy_node()

    # プロセスの終了
    rclpy.shutdown()

if __name__ == "__main__":
    main()
