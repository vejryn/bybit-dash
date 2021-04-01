# Bybit Dash

Simple live dashboard for bybit using pybybit and plotly-dash library. This is modifiable use with another crypto exchange, or another metrics from bybit.

### Installation

```
git clone https://github.com/vejryn/bybit-dash.git
```

### Demo

Demo with debug on.
![demo](https://user-images.githubusercontent.com/22088378/112555990-df718a80-8dfb-11eb-8259-512f0c942f97.gif)


### Recommendation

- Only retrieve new active orders, to get all available active orders, retrieve it from REST API, then update using websocket.
