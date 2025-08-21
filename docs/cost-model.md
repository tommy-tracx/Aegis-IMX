# Cost Model & Scale-Up Path

1. **Initial Deployment**
   - Single region, multi-AZ Kubernetes cluster.
   - Moderate cluster size; on-demand instances for services.
2. **Optimization Phase**
   - Tiered S3 storage for lakehouse (raw/bronze/silver/gold).
   - Spot instances for batch Spark workloads.
   - Autoscaling via HPA and KEDA for Flink.
3. **Scale-Up**
   - Add regions for DR; replicate data with <5m RPO.
   - Increase node pools; shard Kafka/Redpanda clusters.
   - Use reserved instances for baseline workloads.
