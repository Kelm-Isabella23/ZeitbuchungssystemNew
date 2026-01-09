from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from time_tracker.decorators import require_role
from time_tracker.models import RoleRequest


@login_required
def request_vip(request):
    # nur USER darf VIP beantragen
    if request.user.profile.role != "USER":
        return redirect("dashboard")

    # bereits offen?
    if RoleRequest.objects.filter(
        user=request.user, requested_role="VIP", status="PENDING"
    ).exists():
        messages.info(request, "Du hast bereits einen offenen VIP-Antrag.")
        return redirect("dashboard")

    RoleRequest.objects.create(user=request.user, requested_role="VIP")
    messages.success(request, "VIP-Antrag wurde gestellt.")
    return redirect("dashboard")


@login_required
def request_admin(request):
    # nur VIP darf ADMIN beantragen
    if request.user.profile.role != "VIP":
        return redirect("dashboard")

    if RoleRequest.objects.filter(
        user=request.user, requested_role="ADMIN", status="PENDING"
    ).exists():
        messages.info(request, "Du hast bereits einen offenen Admin-Antrag.")
        return redirect("dashboard")

    RoleRequest.objects.create(user=request.user, requested_role="ADMIN")
    messages.success(request, "Admin-Antrag wurde gestellt.")
    return redirect("dashboard")


@require_role("ADMIN")
def admin_requests(request):
    pending = (
        RoleRequest.objects.filter(status="PENDING")
        .select_related("user")
        .order_by("-created_at")
    )

    if request.method == "POST":
        req_id = request.POST.get("req_id")
        action = request.POST.get("action")  # approve / reject

        rr = RoleRequest.objects.filter(id=req_id, status="PENDING").select_related("user").first()
        if rr is None:
            return redirect("admin_requests")

        if action == "approve":
            rr.status = "APPROVED"
            rr.save()

            # Rolle setzen
            profile = rr.user.profile
            profile.role = rr.requested_role
            profile.save()

            messages.success(
                request,
                f"Antrag genehmigt: {rr.user.username} ist jetzt {rr.requested_role}.",
            )
        elif action == "reject":
            rr.status = "REJECTED"
            rr.save()
            messages.info(request, f"Antrag abgelehnt: {rr.user.username}.")
        return redirect("admin_requests")

    return render(
        request,
        "admin_requests.html",
        {"pending": pending, "role": request.user.profile.role},
    )


@require_role("ADMIN")
def admin_users(request):
    users = User.objects.all().select_related("profile").order_by("username")

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")  # block / unblock

        u = User.objects.filter(id=user_id).first()
        if u is None:
            return redirect("admin_users")

        if u.is_superuser:
            messages.error(request, "Superuser kann nicht gesperrt werden.")
            return redirect("admin_users")

        if action == "block":
            u.profile.is_blocked = True
            u.profile.save()
        elif action == "unblock":
            u.profile.is_blocked = False
            u.profile.save()

        return redirect("admin_users")

    return render(
        request,
        "admin_users.html",
        {"users": users, "role": request.user.profile.role},
    )
