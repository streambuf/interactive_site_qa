from ask.models import TopTags, TopUsers

def top_tags_users(request):
	pop_tags = TopTags.objects.all() 
	pop_users = TopUsers.objects.all()           
	return {'pop_tags': pop_tags, 'pop_users': pop_users}
