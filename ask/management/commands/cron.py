# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'askmoiseev.settings'

from django.core.management.base import BaseCommand, CommandError
from loginsys.models import User
from ask.models import Tag, TopTags, TopUsers


class Command(BaseCommand):
 
	def handle(self, *args, **options):
		pop_tags = Tag.objects.raw('''SELECT b.id, COUNT(a.id) as count FROM ask_question_tags a
											INNER JOIN ask_tag AS b ON (a.tag_id = b.id)
											GROUP BY a.tag_id
											ORDER BY count DESC
											LIMIT 20''')
		TopTags.objects.all().delete()									
		for p in pop_tags:
			ptag = TopTags.objects.create(old_id = p.id, content_tag = p.content_tag)
			ptag.save()	
		pop_users = User.objects.raw('''SELECT DISTINCT b.id
											FROM
											( 
											 SELECT id_user_id, question_rating AS rating
											 FROM ask_question 
											 WHERE creation_date_question > '2013-04-14 23:59:59'
											 UNION
											 SELECT id_user_id, answer_rating AS rating
											 FROM ask_answer 
											 WHERE creation_date_answer > '2013-04-14 23:59:59'
											 ORDER BY rating DESC 
											 LIMIT 10
											) AS a
											LEFT JOIN loginsys_user AS b
											ON (a.id_user_id = b.id) ''')
		TopUsers.objects.all().delete()										
		for p in pop_users:
			puser = TopUsers.objects.create(old_id = p.id, username = p.username)
			puser.save()																			
												
