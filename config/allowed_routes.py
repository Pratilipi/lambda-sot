# author entity
author = []

# GET
#author.append('/authors')

# GET and PATCH
author.append('/authors/(\d{16})')

# PATCH
author.append('/authors/(\d{16})/profile_image')
author.append('/authors/(\d{16})/update_facts')

# DELETE
author.append('/authors/(\d{16})/cover_image')
author.append('/authors/(\d{16})/profile_image')

