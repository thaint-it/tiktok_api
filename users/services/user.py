from django.db.models import Q
from users.models import User
from users.serializer.user import UserSerializer
from utils.utils import Utils
from django.contrib.auth.hashers import make_password
from django.conf import settings


class UserService:
    @classmethod
    def get_user(cls, user_id):
        user = User.objects.filter(id=user_id).first()
        return user

    @classmethod
    def update_is_verified(cls, user_id):
        pass

    @classmethod
    def get_users(cls,  page=1, **kwargs):
        filter_by_role = kwargs.get('filter_by_role')
        filter_by_status = kwargs.get('filter_by_status')
        search = kwargs.get('search')
        users = User.objects.all().order_by("-created_at")

        if filter_by_status:
            users = users.filter(status=filter_by_status)

        if filter_by_role:
            users = users.filter(role=filter_by_role)

        if search:
            users = users.filter(
                Q(email__icontains=search) | Q(full_name__icontains=search)
                | Q(phone_number__icontains=search) | Q(ward__name__icontains=search)
            )

        pages, total = Utils.paginator(UserSerializer(users, many=True).data, page)
        return pages, total

    @classmethod
    def create_user(cls, user, **kwargs):
        email = kwargs.get('email')
        user_id = kwargs.get('user_id')
        username = kwargs.get('username')
        password = kwargs.get('password') or settings.DEFAULT_PASSWORD

        # if role == Roles.ADMIN_XA:
        #     exiting_ward_admin = User.objects.filter(ward_id=ward_id, role=Roles.ADMIN_XA).exists()
        #     if exiting_ward_admin:
        #         raise Exception('Admin xã đã tồn tại trước đó.')

        prepare_data = dict(
            email=email,
            user_id=user_id,
            username=username,
            password=make_password(password)
        )

        return User.objects.create(**prepare_data)

    # @classmethod
    # def reset_password(cls, user: User):
    #     message = f"Tôi là {user.full_name}, đang công tác ở {user.ward.name}, tôi gửi email này để yêu cầu cấp lại mật khẩu."
    #     return MailService.send_mail(
    #         subject='Yêu cầu cấp lại mật khẩu',
    #         message=message,
    #         from_email=settings.FROM_EMAIL,
    #         recipient_list=[settings.FROM_EMAIL]
    #     )