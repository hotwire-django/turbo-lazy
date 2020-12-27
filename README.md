# Turbo-Lazy

Basically, it comes down to the following statement:

    {% lazy 'apps.core.partial_views._machine_card' poll_status.machine_id %}
        {% include 'core/partials/_machine_card_loading.html' with name=poll_status.name machine_id=poll_status.machine_id %}
    {% endlazy %}

The content inside the lazy tag is rendered right away in a turbo-frame with a src tag that points to an auto generated URL where the view given lazy controller is called (with the parameters given in the controller). So this can be a slow loading view as its lazy loaded.
This is based on turbo-frames, i.e. the lazy loading is client initiated. With something like turbo-streams (and the django implementation), it would be possible to push the update from the server which would be even cooler (especially a single channel could be used for multiple elements).
So, the page will be rendered as follows:

```{html}
<turbo-frame id="1c87a216-6ad5-4320-861e-261caf3e5dd7" src="/lazy/?token=eyJpZCI6ICIxYzg3YTIxNi02YWQ1LTQzMjAtODYxZS0yNjFjYWYzZTVkZDciLCAidmlldyI6ICJhcHBzLmNvcmUucGFydGlhbF92aWV3cy5fbWFjaGluZV9jYXJkIiwgImFyZ3MiOiBbMV0sICJrd2FyZ3MiOiB7fX0=">   
    <div class="card bg-primary text-white mb-4">
        <div class="card-body">
    
            <b>Machine 1</b>
        
        </div>
        <div class="card-footer" style="height: 7rem;">
            
            <div class="d-flex justify-content-center">
                <div class="spinner-border" role="status">
                    <span class="sr-only">Loading...</span>
                </div>
            </div>
    
        </div>
        <div class="card-footer d-flex align-items-center justify-content-between">
            
            <a class="small text-white stretched-link"
               href="/machine/1/" target="_top">View Details</a>
            <div class="small text-white"><i class="fas fa-angle-right"></i></div>
    
        </div>
    </div>
</turbo-frame>
```

And a call to `/lazy/?token=...` will return the response of calling the view function 
`apps.core.partial_views._machine_card` with given positional argument `poll_status.machine_id` also wrapped inside 
a `<turbo-frame>` tag with the same `id` so that it will automatically swapped by turboframe.

## Release Notes

**0.1.1** - Several minor fixes

**0.1.0** - Initial Release
