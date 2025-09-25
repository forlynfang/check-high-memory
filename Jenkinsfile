pipeline {
    agent any
    stages {
        stage('Enable virtual environment pyats') {
            steps {
                echo 'Setup PYATS environment'
                sh 'python3 -m venv pyats'
                sh 'source pyats/bin/activate'
            }
        }
        stage('List Files in Directory') {
            steps {
                echo 'Confirm required files are cloned'
                sh 'ls -la'
            }
        }        
        stage('Run the Python script apac_high_memory.py') {
            steps {
                
                echo 'Activate Python script to show used memory'
                withCredentials([
                    // 绑定用户名密码凭证到两个环境变量：MY_USERNAME 和 MY_PASSWORD
                    usernamePassword(
                        credentialsId: 'CISCO-ID',
                        usernameVariable: 'CISCO_USERNAME', // 自定义用户名环境变量名
                        passwordVariable: 'CISCO_PASSWORD'  // 自定义密码环境变量名
                    ),
                    usernamePassword(
                        credentialsId: 'FTP-ID',
                        usernameVariable: 'FTP_USERNAME', // 自定义用户名环境变量名
                        passwordVariable: 'FTP_PASSWORD'  // 自定义密码环境变量名
                    ),
                    string(
                        credentialsId: 'Jenkins_webhook',
                        variable: 'TEAMS_WEBHOOK' // 自定义密钥环境变量名
                    )
                ]) {
                    // 在这个块内的所有步骤都可以访问到上面定义的环境变量
                    echo "Username is $CISCO_USERNAME"
                    echo "Password is $CISCO_PASSWORD" // Jenkins 会自动用 **** 屏蔽值
                   
                    // 执行你的 Python 脚本
                    sh 'python3 apac_high_memory.py --testbed apac_tb.yaml'
                }   
            }
        }
    }
    post {
        always {
            cleanWs(cleanWhenNotBuilt: true,
                    deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true)
        }
    }
}
