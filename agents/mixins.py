from django.contrib.auth.mixins import AccessMixin


class AgentManagerAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and an agent manager."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_agent_manager:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
