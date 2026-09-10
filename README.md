# Projeto Robô SCARA - Simulação no ROS 2 e Gazebo

Este repositório contém a modelagem, simulação física e os controladores de um robô SCARA equipado com uma garra de dois dedos. O projeto foi desenvolvido utilizando ROS 2 (Humble), Gazebo e `ros2_control`.

## 1.Clonar o Repositório

Para que o sistema de compilação do ROS 2 funcione corretamente, você deve clonar este repositório obrigatoriamente dentro da pasta src de qualquer pasta na area de trabalho. 

Abra o terminal e siga os passos abaixo para criar o workspace e clonar os arquivos:

bash
# Crie a pasta do workspace e a pasta src
mkdir -p ~/scara_ws/src
cd ~/scara_ws/src

# Clone o repositório (substitua a URL abaixo pelo link do seu GitHub)
git clone [https://github.com/Lonesome-fish/project-scara-arm-ros2/new/main?filename=README.md


# Atualiza a lista do rosdep (necessário inicializar com 'sudo rosdep init' se for a primeira vez)
rosdep update

# Lê os arquivos do projeto e baixa automaticamente o que faltar
rosdep install --from-paths src --ignore-src -r -y

Comandos para controle do projeto

#ros2 launch scara_description Scara.launch.py:
  Abre o programa rviz para visualização do braço scara, com menu adicional de sliders para observar a movimentação. Ele vai abrir vazio, basta ir na aba superior em open file, o arquivo rviz deste projeto ja esta incluido dentro do repositorio

#ros2 launch scara_description Gazebo.launch.py:
  Abri o simulador gazebo com o braço scara para simulação

#ros2 launch scara_controller Controller.launch.py:
  Deve ser inicializado apos o gazebo, permite o controle do robo por um terceiro terminal

#Python3 Demo.py
  Em um terceiro terminal com o gazebo e controlador ja iniciados, este comando vai mandar 10 posições para o braço scara assumir dentro do simulador, para uma demonstração
