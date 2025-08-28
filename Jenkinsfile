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
                sh 'python3 apac_high_memory.py --testbed apac_tb.yaml'
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
