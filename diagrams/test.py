from diagrams import Diagram, Edge, Cluster
from diagrams.custom import Custom
from diagrams.gcp.compute import GCF
from diagrams.gcp.analytics import BigQuery
from diagrams.gcp.storage import GCS

from diagrams.aws.storage import S3

with Diagram("Cross Cloud Unified SQL Data Pipeline", show=False):

    with Cluster("GCP"):
        with Cluster("BigQuery"):
            bqrf_remove_html_tags = Custom("remove_html_tags\n(Remote Function)", "../images/icons/generic/function.png")
            bqrm_vision = Custom("vision\n(Remote Model)", "../images/icons/generic/ai-model.png")
            bqrm_onnx = Custom("onnx_model\n(Remote Model)", "../images/icons/generic/ai-model.png")
            biglake_table = Custom("BigLake Table", "../images/icons/generic/table.png")
            object_table = Custom("Object Table", "../images/icons/generic/table.png")

        with Cluster("Google Cloud Storage"):
            pictures = Custom("*.png", "../images/icons/generic/pictures.png")
            onnx_file = Custom("ONNX file", "../images/icons/generic/ai-model-2.png")

        gcf = GCF("remove_html_tags")
        cloud_vision = Custom("Cloud Vision", "../images/icons/gcp/cloud-vision-api.png")

    with Cluster("AWS", graph_attr={"bgcolor": "#eeeeee"}):
        s3 = S3("*.csv")

    object_table >> Edge() << pictures
    bqrm_vision >> Edge() << cloud_vision
    bqrm_onnx >> Edge() << onnx_file
    bqrf_remove_html_tags >> Edge(label="1. Pass data to GCF through CONNECTION") >> gcf
    bqrf_remove_html_tags << Edge(label="2. Pass processed data back to BQ") << gcf
    
    biglake_table >> Edge() << s3

with Diagram("RAG", show=False):
    website = Custom("Website", "../images/icons/generic/landing-page.png")
    user = Custom("User", "../images/icons/generic/programmer.png")
    with Cluster("GCP"):
        document_ai = Custom("layout-parser-processor\n(Document AI)", "../images/icons/gcp/document-ai.png")
        embedding_model = Custom("text-embedding-004\n(Vertex AI)", "../images/icons/gcp/vertexai.png")
        text_model = Custom("gemini-1.5-flash-002\n(Vertex AI)", "../images/icons/gcp/vertexai.png")
        with Cluster("BigQuery"):
            doc_parser_bqrm = Custom("doc_parser\n(Remote Model)", "../images/icons/generic/ai-model.png")
            embedding_model_bqrm = Custom("embedding_model\n(Remote Model)", "../images/icons/generic/ai-model.png")
            text_model_bqrm = Custom("text_model\n(Remote Model)", "../images/icons/generic/ai-model.png")
            pdf = Custom("pdf\n(Object Table)", "../images/icons/generic/table.png")
            chunked_pdf = Custom("chunked_pdf", "../images/icons/generic/table.png")
            parsed_pdf = Custom("parsed_pdf", "../images/icons/generic/table.png")
            embeddings = Custom("embeddings", "../images/icons/generic/table.png")
        with Cluster("GCS"):
            pdf_file = Custom(".pdf", "../images/icons/generic/pdf-file.png")

        pdf >> Edge(color="red") >> doc_parser_bqrm >> Edge(color="red") >> chunked_pdf \
            >> Edge(color="red") >> parsed_pdf \
            >> Edge(color="red") >> embedding_model_bqrm >> Edge(color="red") >> embeddings

        text_model_bqrm >> Edge() << text_model
        pdf >> Edge() << pdf_file
        doc_parser_bqrm >> Edge() << document_ai
        embedding_model_bqrm >> Edge() << embedding_model

        user >> website >> Edge(color="green") >> embedding_model_bqrm \
             >> Edge(color="green") >> embeddings >> Edge(color="green") >> text_model_bqrm
        website >> Edge(color="green") >> text_model_bqrm