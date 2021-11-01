@Library('jenkins-shared-library@release') _

pipeline {

    agent {
        label 'buildah'
    }

    options {
        skipStagesAfterUnstable()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '28'))
        timeout(time: 1, unit: 'HOURS')
        timestamps()
    }

    stages {
        stage("Build and Push") {
            steps {
                notifyBitbucket state: "INPROGRESS"
                script {
                    currentBuild.description = GIT_COMMIT
                    env.branch_name_slug = env.BRANCH_NAME.replaceAll('[^a-zA-Z0-9._-]+','')
                    echo "Branch name slug is: ${env.branch_name_slug}"
                }
                containerBuild(path: 'apiserver', dockerFileName: 'Dockerfile', repository: 'devops/oim-api-apiserver', tags: ['latest', GIT_COMMIT, "${env.branch_name_slug}"])
            }
        }

        // stage("Deploy to TEST") {
        //     when {
        //         branch 'master'
        //     }
        //     steps {
        //         containerDeploy(repositoryName: 'example-non-prod', file: 'demo-app-test/values.yaml', yamlPatches: ["generic.image.tag": "${GIT_COMMIT}"])
        //     }
        // }
    }

    post {
        success {
            notifyBitbucket state: "SUCCESSFUL"
        }

        // fixed {
        //     mailTo status: "SUCCESS", actuator: true, recipients: [], logExtract: true
        // }

        unsuccessful {
            notifyBitbucket state: "FAILED"
            // mailTo status: "FAILURE", actuator: true, recipients: [], logExtract: true
        }
    }
}