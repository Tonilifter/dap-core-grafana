FROM grafana/grafana:6.6.0

COPY ./configuration/providers/grafana-dashboard-provider.yml /etc/grafana/provisioning/dashboards
# COPY ./configuration/dashboards /var/lib/grafana/dashboards
# COPY ./configuration/notifiers /etc/grafana/provisioning/notifiers

EXPOSE 3000

ENTRYPOINT ["/run.sh"]