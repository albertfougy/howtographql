import graphene
from graphene_django import DjangoObjectType

from .models import Link


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()


class CreateLink(graphene.Mutation):
    '''
    Defines a mutation class. Right after, you define the output of the mutation, 
    the data the server can send back to the client. The output is defined field 
    by field for learning purposes. In the next mutation you’ll define them as just one.
    '''
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    class Arguments:
        '''
        Defines the data you can send to the server, in this case, 
        the links’ url and description.
        '''
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info, url, description):
        '''
        The mutation method: it creates a link in the database using the data 
        sent by the user, through the url and description parameters. After, 
        the server returns the CreateLink class with the data just created. 
        See how this matches the parameters set on #1.
        '''
        link = Link(url=url, description=description)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
        )

class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()