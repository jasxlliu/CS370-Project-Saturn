CREATE TABLE SoundList (
	Title VARCHAR(50) NOT NULL UNIQUE,
    Length FLOAT NOT NULL,
    IsEdited BOOLEAN NOT NULL,
    DateCreated DATETIME NOT NULL,
    PRIMARY KEY(Title)
);

CREATE TABLE SoundPlaylistsInfo (
	SoundTitle VARCHAR(50) NOT NULL,
    PlaylistTitle VARCHAR (25),
    PRIMARY KEY(SoundTitle, PlaylistTitle),
    FOREIGN KEY(SoundTitle) REFERENCES SoundList(Title)
);