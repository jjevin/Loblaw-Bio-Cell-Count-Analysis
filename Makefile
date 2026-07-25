setup:
	pip install -r requirements.txt 

pipeline:
	python load_data.py
	python pipeline.py

dashboard:
	python load_data.py
	streamlit run dashboard.py
