FROM tensorflow/serving
ADD dx-classifier /models/dx-classifier
ENV MODEL_NAME=dx-classifier
CMD tensorflow_model_server \
  --port=8500 \
  --rest_api_port=8501 \
  --model_name=dx-classifier \
  --model_base_path=/models/dx-classifier
