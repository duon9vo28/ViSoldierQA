# 📌 Deploy The Model Using FastAPI

## 🔍 What are contained in each folder?
- 📂 **config**: Configuration for the model and the logger

- 📂 **logs**: Logging info, including the api log, data log and model log.

- 📂 **middle_ware**: CORS middle_ware and HTTP middle_ware

- 📂 **models**: Define the model structure 

- 📂 **processor**: Define the processors to handling the raw input.

- 📂 **routes**: Define the routers

- 📂 **schemas**: Define the pydantic model for the input.

- 📂 **test_data**: Some data to test the model

- 📂 **utils**: Define the customized logger

- 📂 **weights**: Model parameters

- 📄 *requirements.txt*: Required libraries to run the model

---


## 🛠️ Deploy the model

- Install the required libraries (if needed): `pip install -r requirements.txt`

- Host your server: `python server.py` 
or `uvicorn app:app`

- Access the address `http://localhost:8000/docs` or `http://127.0.0.1:8000/docs` to view the results.# ViSoldierQA
