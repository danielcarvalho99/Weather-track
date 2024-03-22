# Weather-Track #
Projeto que visa manter registro das temperaturas de uma determinada cidade por meio de um DAG do Airflow. Na ocasião, foi utilizada a minha cidade natal, Aracaju. Para obter esses dados, foi utilizada a API OpenWeather, que fornece
um arquivo JSON informando as informações sobre o tempo na localidade buscada.

A informação é coletada de hora em hora, e o grafo do processo é o seguinte:

![dag](https://github.com/danielcarvalho99/Weather-track/assets/40178648/a08dc90c-74c9-4c38-b27a-5780c91fd757)

Os dados são exibidos por meio do log da aplicação:

![climate](https://github.com/danielcarvalho99/Weather-track/assets/40178648/0cfd68cc-6530-4a82-9f61-7e69ed9406a9)
