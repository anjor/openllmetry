"""Unit tests configuration module."""

import pytest
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.instrumentation.watsonx import WatsonxInstrumentor
from ibm_watsonx_ai.foundation_models import ModelInference

pytest_plugins = []


@pytest.fixture(scope="session")
def exporter():
    exporter = InMemorySpanExporter()
    processor = SimpleSpanProcessor(exporter)

    provider = TracerProvider()
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    WatsonxInstrumentor().instrument()

    return exporter


@pytest.fixture(autouse=True)
def clear_exporter(exporter):
    exporter.clear()


@pytest.fixture
def watson_ai_model():
    watsonx_ai_model = ModelInference(
        model_id="google/flan-ul2",
        project_id="c1234567-2222-2222-3333-444444444444",
        credentials={
                "apikey": "test_api_key",
                "url": "https://us-south.ml.cloud.ibm.com"
                },
    )
    return watsonx_ai_model


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": ["authorization"],
        "allow_playback_repeats": True,
        "decode_compressed_response": True,
        }
