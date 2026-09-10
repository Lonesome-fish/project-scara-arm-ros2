#!/usr/bin/env python3
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

class ScaraDemoNode(Node):
    def __init__(self):
        super().__init__('scara_demo_node')
        self.arm_pub = self.create_publisher(Float64MultiArray, '/arm_controller/commands', 10)
        self.gripper_pub = self.create_publisher(Float64MultiArray, '/gripper_controller/commands', 10)
        time.sleep(1.0)
        self.get_logger().info("Iniciando a sequencia de demonstracao do Robo SCARA...")

    def publish_arm(self, positions):
        msg = Float64MultiArray()
        msg.data = positions
        for _ in range(5):
            self.arm_pub.publish(msg)
            time.sleep(0.1)

    def publish_gripper(self, position):
        msg = Float64MultiArray()
        # Envia 1 único valor para a garra (a junta mimica faz o resto)
        msg.data = [position]
        for _ in range(5):
            self.gripper_pub.publish(msg)
            time.sleep(0.1)

    def run_sequence(self):
        # Abertura maxima da garra definida como 0.3 para ficar bem perceptivel no Gazebo
        waypoints = [
            {'desc': '1. Posicao Home (Garra Aberta em 0.3)', 'arm': [0.0, 0.0, 0.0, 0.0], 'gripper': 0.3, 'wait': 3.0},
            {'desc': '2. Mover para Posicao A', 'arm': [0.8, -1.2, -0.02, 0.0], 'gripper': 0.3, 'wait': 3.0},
            {'desc': '3. Baixar Z (Aproximacao)', 'arm': [0.8, -1.2, -0.12, 0.0], 'gripper': 0.3, 'wait': 2.5},
            {'desc': '4. Fechar garra (0.0)', 'arm': [0.8, -1.2, -0.12, 0.0], 'gripper': 0.0, 'wait': 2.0},
            {'desc': '5. Elevar Z com objeto', 'arm': [0.8, -1.2, -0.02, 0.0], 'gripper': 0.0, 'wait': 2.5},
            {'desc': '6. Mover para Posicao B', 'arm': [-0.8, 1.0, -0.02, 0.0], 'gripper': 0.0, 'wait': 3.5},
            {'desc': '7. Baixar Z na Posicao B', 'arm': [-0.8, 1.0, -0.12, 0.0], 'gripper': 0.0, 'wait': 2.5},
            {'desc': '8. Abrir garra (0.3)', 'arm': [-0.8, 1.0, -0.12, 0.0], 'gripper': 0.3, 'wait': 2.0},
            {'desc': '9. Retornar ao Home', 'arm': [0.0, 0.0, 0.0, 0.0], 'gripper': 0.3, 'wait': 3.0}
        ]

        for step in waypoints:
            self.get_logger().info(f"==> {step['desc']}")
            self.publish_arm(step['arm'])
            self.publish_gripper(step['gripper'])
            time.sleep(step['wait'])

        self.get_logger().info("Demonstracao concluida com sucesso!")

def main(args=None):
    rclpy.init(args=args)
    node = ScaraDemoNode()
    try:
        node.run_sequence()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
