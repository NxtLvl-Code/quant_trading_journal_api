from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from journal.models import Profile, Tag, Trade
from django.utils.dateparse import parse_datetime
import json

class Command(BaseCommand):
    help = "Import legacy data (JSON). Expected structure: {users:[], tags:[], trades:[]}"

    def add_arguments(self, parser):
        parser.add_argument('json_path', type=str, help='Path to legacy JSON export')

    def handle(self, *args, **options):
        path = options['json_path']
        try:
            with open(path, 'r') as f:
                data = json.load(f)
        except Exception as e:
            raise CommandError(f"Failed to read JSON: {e}")

        users = data.get('users', [])
        tags = data.get('tags', [])
        trades = data.get('trades', [])

        # Import users
        user_map = {}  # legacy id -> Django User
        for u in users:
            email = u.get('email') or ''
            username = u.get('username') or (email.split('@')[0] if email else f"user{u.get('id','')}")
            first_name = u.get('first_name') or ''
            last_name = u.get('last_name') or ''
            user_obj, _ = User.objects.get_or_create(username=username, defaults={'email': email, 'first_name': first_name, 'last_name': last_name})
            user_map[str(u.get('id'))] = user_obj

        # Import tags
        tag_map = {}  # legacy id or name -> Tag
        for t in tags:
            name = t.get('tag_name') or t.get('name') or t.get('tag')
            if not name:
                continue
            tag_obj, _ = Tag.objects.get_or_create(tag_name=name)
            key = str(t.get('id')) if t.get('id') is not None else name
            tag_map[key] = tag_obj

        # Import trades
        created = 0
        for tr in trades:
            # user
            legacy_uid = str(tr.get('user_id')) if tr.get('user_id') is not None else None
            user = user_map.get(legacy_uid) if legacy_uid else None
            if not user:
                # fallback to first user or create a default
                user = User.objects.first() or User.objects.create(username='default')

            # fields
            asset_symbol = tr.get('asset_symbol') or tr.get('symbol') or ''
            side = (tr.get('side') or '').upper()[:5] or 'BUY'
            quantity = tr.get('quantity')
            price = tr.get('price')
            trade_time = tr.get('trade_time')
            if isinstance(trade_time, str):
                trade_time = parse_datetime(trade_time.replace('Z', '+00:00'))

            trade = Trade.objects.create(
                user=user,
                asset_symbol=asset_symbol,
                side=side,
                quantity=quantity if quantity not in (None, '') else None,
                price=price if price not in (None, '') else None,
                trade_time=trade_time,
                notes=tr.get('notes') or None
            )

            # tags on trade
            legacy_tag_ids = tr.get('tag_ids') or tr.get('tags') or []
            # accept [id,...] or [{'id':..},...] or [{'tag_name':..}, ...]
            resolved = []
            for t in legacy_tag_ids:
                if isinstance(t, dict):
                    key = str(t.get('id')) if t.get('id') is not None else (t.get('tag_name') or t.get('name'))
                else:
                    key = str(t)
                if key in tag_map:
                    resolved.append(tag_map[key])
            if resolved:
                trade.tags.set(resolved)

            created += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {len(users)} users, {len(tags)} tags, {created} trades"))
