# 实现了相对路径文件映射，GPU直通
docker run -it -v ${PWD}/docker_result/code_inspection_result/logs:/app/logs  --gpus all privacy_compliance_image