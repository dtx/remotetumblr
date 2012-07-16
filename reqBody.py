class reqBodyMaker:
    def makeBody(self,args):
        print args.type
        post = {
            'type': args.type,
            'state': args.state,
            'tags': args.tags,
            'tweet': args.tweet,
            'markdown': args.markdown,
            'filename': args.filename
        }
        #removing all the None values and replacing them with empty strings.
        # can also just delete, them, i dont know.
        for k in post.keys():
            if post[k] is None:
                post[k]=''

        return post
