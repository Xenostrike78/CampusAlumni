from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
import datetime
from django.db.models import Value, CharField,Q
from django.db.models.functions import Concat
from .models import User, College, Post, ProfessionalExperience, Certification, CollegeNetworkRequest, UserConnection

@login_required
def connections(request):
    """Connections view to show incoming and sent connection requests."""
    incoming_requests = UserConnection.objects.filter(to_user=request.user, status='pending')
    sent_requests = UserConnection.objects.filter(from_user=request.user, status='pending')
    context = {
        'incoming_requests': incoming_requests,
        'sent_requests': sent_requests,
    }
    return render(request, 'connections.html', context)

def home(request):
    """Landing page view."""
    return render(request, 'index.html')




def login_view(request):
    """Login view."""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('community_feed')  # Changed redirect to community_feed
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')

def signup_view(request):
    """Signup view."""
    if request.method == 'POST':
        # Process form data
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Create user (simplified for now)
        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            return redirect('edit_profile')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'signup.html')

def logout_view(request):
    """Logout view."""
    logout(request)
    return redirect('home')

@login_required
def edit_profile(request):
    """Edit profile view."""
    user = request.user
    if request.method == 'POST':
        # Update user profile with form data
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.short_bio = request.POST.get('short_bio', user.short_bio)
        user.current_job = request.POST.get('current_role', user.current_job)
        user.industry = request.POST.get('industry', user.industry)
        user.graduation_year = request.POST.get('gradYear', user.graduation_year)
        user.degree = request.POST.get('degree', user.degree)
        user.location = request.POST.get('location', user.location)
        user.skills = request.POST.get('skills', user.skills)
        user.linkedin_url = request.POST.get('linkedin_url', user.linkedin_url)
        user.contact_email = request.POST.get('contactEmail', user.contact_email)
        user.is_mentor = request.POST.get('mentorOptIn', False) == 'on'
        user.mentor_bio = request.POST.get('mentorBio', user.mentor_bio)
        user.areas_of_expertise = ','.join(request.POST.getlist('mentorExpertise'))  # multiple select stored as comma-separated string
        user.join_college_network = request.POST.get('networkOptIn', False) == 'on'
        user.directory_visible = request.POST.get('directoryVisible', False) == 'on'
        user.show_contact_info = request.POST.get('showContactInfo', False) == 'on'
        
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        
        # Removed certification saving as certifications section is removed
        
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    
    return render(request, 'edit-profile.html', {'user': user})




@login_required
def alumni_directory(request):
    """Alumni directory view with search and filters."""
    query = request.GET.get('name', '')
    university = request.GET.get('university', '')
    industry = request.GET.get('industry', '')
    graduation_year = request.GET.get('graduation_year', '')

    # alumni = User.objects.all()
    alumni = User.objects.annotate(
        search_name=Concat('first_name', Value(' '), 'last_name', output_field=CharField())
    )

    if query:
        print(query)
        # Filter manually on first_name and last_name without using Q objects
        alumni = alumni.filter(Q(search_name__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
        print(alumni)
    if university:
        alumni = alumni.filter(college__name__icontains=university)
    if industry:
        alumni = alumni.filter(industry__icontains=industry)
    if graduation_year:
        current_year = datetime.date.today().year
        try:
            if graduation_year == 'recent-5':
                alumni = alumni.filter(graduation_year__gte=current_year - 4)
            elif graduation_year == 'previous-10':
                alumni = alumni.filter(graduation_year__lt=current_year - 4, graduation_year__gte=current_year - 14)
            elif graduation_year.startswith('before-'):
                year_limit = int(graduation_year.split('-')[1])
                alumni = alumni.filter(graduation_year__lt=year_limit)
            else:
                year = int(graduation_year)
                alumni = alumni.filter(graduation_year=year)
        except ValueError:
            pass

    alumni = alumni.exclude(id=request.user.id).order_by('first_name')

    # Add mentor expertise list attribute to each user for template use
    for alum in alumni:
        areas_of_expertise = alum.areas_of_expertise
        if isinstance(areas_of_expertise, str):
            alum.mentor_expertise = areas_of_expertise.split(',')
        else:
            alum.mentor_expertise = []

    distinct_colleges = User.objects.values_list('college__name', flat=True).distinct()
    distinct_industries = User.objects.values_list('industry', flat=True).distinct()

    current_year = datetime.date.today().year
    recent_5_years = [str(y) for y in range(current_year, current_year - 5, -1)]
    previous_10_years = [str(y) for y in range(current_year - 5, current_year - 15, -1)]

    # Get connection statuses for current user and alumni users
    

    connection_statuses = {}
    if request.user.is_authenticated:
        connections = UserConnection.objects.filter(
            Q(from_user=request.user, to_user__in=alumni) |
            Q(to_user=request.user, from_user__in=alumni)
        )
        for conn in connections:
            if conn.from_user == request.user:
                connection_statuses[conn.to_user.id] = conn.status
            else:
                connection_statuses[conn.from_user.id] = conn.status

    context = {
        'alumni': alumni,
        'Name': query,
        'university': university,
        'industry': industry,
        'graduation_year': graduation_year,
        'distinct_colleges': distinct_colleges,
        'distinct_industries': distinct_industries,
        'recent_5_years': recent_5_years,
        'previous_10_years': previous_10_years,
        'connection_statuses': connection_statuses,
    }
    return render(request, 'alumni-directory.html', context)

@login_required
def community_feed(request):
    """Community feed view."""
    
    user_college = None
    if request.user and request.user.is_authenticated:
        try:
            user_college = request.user.college
        except Exception:
            user_college = None

    # Fetch user's accepted connections (both directions)
    connections_sent = UserConnection.objects.filter(from_user=request.user, status='accepted').values_list('to_user', flat=True)
    connections_received = UserConnection.objects.filter(to_user=request.user, status='accepted').values_list('from_user', flat=True)
    connected_user_ids = set(connections_sent).union(set(connections_received))

    filter_option = request.GET.get('filter', 'all')

    if filter_option == 'my_college':
        posts = Post.objects.filter(user__college=user_college).order_by('-created_at')
    elif filter_option == 'my_connections':
        posts = Post.objects.filter(user__id__in=connected_user_ids).order_by('-created_at')
    else:  # 'all' or any other value
        posts = Post.objects.all().order_by('-created_at')

    if request.method == 'POST':
        # Create a new post
        content = request.POST.get('content')
        hashtags = request.POST.get('hashtags', '')
        media = request.FILES.get('media')
        
        if content:
            post = Post.objects.create(
                user=request.user,
                content=content,
                hashtags=hashtags,
                media=media
            )
            return redirect('community_feed')
    
    # People you may know: users from the same college who are not connected and not the user
    people_you_may_know = User.objects.filter(college=user_college).exclude(id__in=connected_user_ids).exclude(id=request.user.id)[:5]

    # Get connection requests sent by the user to suggested people
    sent_requests = UserConnection.objects.filter(from_user=request.user, to_user__in=people_you_may_know).values_list('to_user', 'status')
    sent_requests_dict = {user_id: status for user_id, status in sent_requests}
    context = {
        'posts': posts,
        'people_you_may_know': people_you_may_know,
        'user_college': user_college,
        'user': request.user,
        'filter_option': filter_option,
        'sent_requests': sent_requests_dict,
    }
    return render(request, 'community-feed.html', context)

@login_required
def send_connection_request(request, user_id):
    """Send a connection request from the logged-in user to another user."""
    if request.method == 'POST':
        to_user = get_object_or_404(User, id=user_id)
        from_user = request.user
        # Check if connection already exists
        existing_connection = UserConnection.objects.filter(from_user=from_user, to_user=to_user).first()
        if existing_connection:
            if existing_connection.status != 'pending':
                existing_connection.status = 'pending'
                existing_connection.save()
        else:
            UserConnection.objects.create(from_user=from_user, to_user=to_user, status='pending')
        # Redirect back to the referring page
        next_url = request.META.get('HTTP_REFERER', 'community_feed')
        return redirect(next_url)
    return redirect('community_feed')


@login_required
def accept_connection_request(request, request_id):
    """Send a connection request from the logged-in user to another user."""
    if request.method == 'POST':
        to_user = request.user
        from_user = get_object_or_404(User, id=request_id)
        # Check if connection already exists
        connection = UserConnection.objects.filter(from_user=from_user, to_user=to_user, status='pending').first()
        print(connection)
        if connection:
            connection.status = 'accepted'
            connection.save()
        # Redirect back to the referring page
        return redirect('connections')
    return redirect('connections')

@login_required
def profile(request, user_id=None):
    """Profile view to show user's details. If user_id is None, show logged-in user's profile."""
    if user_id:
        # Viewing another user's profile
        user = get_object_or_404(User, id=user_id)
        is_own_profile = (user == request.user)
    else:
        # Viewing own profile
        user = request.user
        is_own_profile = True

    # Count connections (accepted)
    connections_sent = UserConnection.objects.filter(from_user=user, status='accepted').count()
    connections_received = UserConnection.objects.filter(to_user=user, status='accepted').count()
    total_connections = connections_sent + connections_received

    # Prepare mentor expertise as list if stored as string
    areas_of_expertise = user.areas_of_expertise
    if isinstance(areas_of_expertise, str):
        areas_of_expertise = areas_of_expertise.split(',')

    context = {
        'user': user,
        'total_connections': total_connections,
        'mentor_expertise': areas_of_expertise,
        'is_own_profile': is_own_profile,
    }
    return render(request, 'Profile.html', context)


@login_required
def add_experience(request):
    """Add professional experience view."""
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        company_name = request.POST.get('company_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')
        
        if job_title and company_name and start_date:
            ProfessionalExperience.objects.create(
                user=request.user,
                job_title=job_title,
                company_name=company_name,
                start_date=start_date,
                end_date=end_date if end_date else None,
                description=description
            )
            messages.success(request, 'Experience added successfully.')
            return redirect('edit_profile')
    
    return redirect('edit_profile')
