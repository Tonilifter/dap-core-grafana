FROM grafana/grafana:6.7.1

COPY ./configuration/providers/grafana-dashboard-provider.yml /etc/grafana/provisioning/dashboards
# COPY ./configuration/dashboards /var/lib/grafana/dashboards
# COPY ./configuration/notifiers /etc/grafana/provisioning/notifiers

RUN grafana-cli --pluginsDir "/var/lib/grafana/plugins" plugins install grafana-piechart-panel; 
RUN grafana-cli --pluginsDir "/var/lib/grafana/plugins" plugins install natel-plotly-panel; 

EXPOSE 3000

ENTRYPOINT ["/run.sh"]