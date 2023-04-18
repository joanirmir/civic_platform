def get_object(model, pk):
    """
    internal method:
    Get db entry and return instance,
    otherwise, raise 404
    """
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise Http404