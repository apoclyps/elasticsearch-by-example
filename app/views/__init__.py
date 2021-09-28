from app.views.docs import blueprint as docs  # NOQA: F401
from app.views.errors import blueprint as errors  # NOQA: F401
from app.views.healthz import (  # NOQA: F401
    blueprint as healthz,
    blueprint_public as healthz_public,
)
