from django.shortcuts import render, redirect
from .model import AirportRoute
from .form import AirportRouteForm, SearchForm

# add airport node
def add_route(request):
    """Add a new airport route"""
    form = AirportRouteForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("dashboard")

    return render(request, "addRoute.html", {"form": form})



def dashboard(request):
    """Main dashboard view with all functionalities"""
    
    # Ensure root node "Airport A" exists
    root = AirportRoute.objects.filter(parent_airport=None).first()
    if not root:
        AirportRoute.objects.create(
            parent_airport=None, 
            airport_code="Airport A", 
            position="Root",
            duration=0
        )
        root = AirportRoute.objects.filter(parent_airport=None).first()
    

    # Get all airports excluding the root (since root typically has duration=0)
    non_root_airports = AirportRoute.objects.exclude(parent_airport=None)
    
    if non_root_airports.exists():
        # Order by duration descending to get the highest duration first
        longest = non_root_airports.order_by("-duration").first()
    else:
        longest = None
  
    # Exclude root node to avoid always getting Airport A with duration=0
    if non_root_airports.exists():
        # Order by duration ascending to get the lowest duration first
        shortest = non_root_airports.order_by("duration").first()
    else:
        shortest = None

    #Last Reachable Node (Search Form)
    last_node = None
    searchForm = SearchForm(request.POST or None)
    
    if request.method == "POST" and searchForm.is_valid():
        node = searchForm.cleaned_data["airport"]
        direction = searchForm.cleaned_data["direction"]
        current = node
        
        # Traverse in the selected direction until no more nodes exist
        while True:
            next_node = AirportRoute.objects.filter(
                parent_airport=current, 
                position=direction
            ).first()
            if not next_node:
                break
            current = next_node
        
        last_node = current
    
    # Count total airports (excluding root)
    total_airports = non_root_airports.count()
    
    context = {
        "searchForm": searchForm,
        "last_node": last_node,
        "longest": longest,
        "shortest": shortest,
        "total_airports": total_airports,
        "root": root,
    }
    
    return render(request, "dashboard.html", context)


def clear_tree(request):
    """Clear all airport routes"""
    if request.method == "POST":
        AirportRoute.objects.all().delete()
    return redirect("dashboard")