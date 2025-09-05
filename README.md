git clone https://github.com/cleve703/price_predictor
cd price_predictor
docker build -t sl_price_predictor .
docker run -p 8501:8501 sl_price_predictor
open browser to http://0.0.0.0:8501
Username: jsmith
Password: abc
Enter specifications on potential house for investment and click Submit.
Predicted price will appear.
