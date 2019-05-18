"""Database standardization for text tokens.

Classes
-------
Token
    Text token data model with matching-related features.
"""
import typing

from bson.objectid import ObjectId

from tesserae.db.entities.entity import Entity


class Token(Entity):
    """An atomic piece of text, along with related features.

    Tokens contain the atomic pieces of text that inform Matches and make
    up Units. In addition to the raw text, the normalized form of the text
    and features like lemmata and semantic meaning are also part of a
    token.

    Parameters
    ----------
    id : bson.objectid.ObjectId, optional
        Database id of the text. Should not be set locally.
    text : str or bson.objectid.ObjectId, optional
        The text containing this token.
    index : int, optional
        The order of this token in the text.
    display : str, optional
        The un-altered form of this token, as it appears in the original
        text.
    feature_set : bson.objectid.ObjectId, optional
        Database id of the features associated with this token. This should be
        generated by the MongoDB instance on insert.


    Attributes
    ----------
    id : bson.objectid.ObjectId
        Database id of the text. Should not be set locally.
    text : str or bson.objectid.ObjectId
        The text containing this token.
    index : int
        The order of this token in the text.
    display : str
        The un-altered form of this token, as it appears in the original
        text.
    feature_set : bson.objectid.ObjectId
        Database id of the features associated with this token. This should be
        generated by the MongoDB instance on insert.

    """

    collection = 'tokens'

    def __init__(self, id=None, text=None, index=None, display=None,
                 feature_set=None, line=None, phrase=None, frequency=None):
        super(Token, self).__init__(id=id)
        self.text: typing.Optional[typing.Union[Entity, ObjectId]] = text
        self.index: typing.Optional[int] = index
        self.display: typing.Optional[str] = display
        self.feature_set: typing.Optional[typing.Union[Entity, ObjectId]] = feature_set
        self.line: typing.Optional[typing.Union[Entity, ObjectId]] = line
        self.phrase: typing.Optional[typing.Union[Entity, ObjectId]] = phrase
        self.frequency: typing.Optional[typing.Union[Entity, ObjectId]] = frequency

    def match(self, other, feature):
        """Determine whether two tokens match along a given feature.

        Parameters
        ----------
        other : tesserae.db.entities.Token
            The token to compare against.
        feature : {'form','lemmata','semantic','lemmata + semantic','sound'}
            The feature to compare on.

        Returns
        -------
        match : bool
        """
        if feature == 'word':
            return self.form == other.form
        elif feature == 'lemmata':
            return len(set(self.lemmata) & set(other.lemmata)) > 0
        elif feature == 'semantic':
            return len(set(self.semantic) & set(other.semantic)) > 0
        elif feature == 'sound':
            return len(set(self.sound) & set(other.sound)) > 0
        else:
            return len(set(self.lemmata) & set(other.lemmata)) > 0 and \
                   len(set(self.semantic) & set(other.semantic)) > 0

    def json_encode(self, exclude=None):
        self._ignore = [self.text, self.feature_set, self.line, self.phrase, self.frequency]
        self.text = self.text.id if self.text is not None else None
        self.feature_set = self.feature_set.id if self.feature_set is not None else None
        self.line = self.line.id if self.line is not None else None
        self.phrase = self.phrase.id if self.phrase is not None else None
        self.frequency = self.frequency.id if self.frequency is not None else None

        obj = super(Token, self).json_encode(exclude=exclude)

        self.text = self._ignore[0]
        self.feature_set = self._ignore[1]
        self.line = self._ignore[2]
        self.phrase = self._ignore[3]
        self.frequency = self._ignore[4]
        del self._ignore

        return obj

    def unique_values(self):
        uniques = {
            'text': self.text.id if isinstance(self.text, Entity) else self.text,
            'index': self.index
        }
        return uniques
