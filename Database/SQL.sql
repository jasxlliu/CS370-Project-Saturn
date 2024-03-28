CREATE TABLE SoundPlaylistsInfo (
	SoundTitle VARCHAR(50) NOT NULL,
    PlaylistTitle VARCHAR (25),
    PRIMARY KEY(SoundTitle, PlaylistTitle)
);

CREATE TABLE SoundList (
	Title VARCHAR(50) NOT NULL UNIQUE,
    Length FLOAT NOT NULL,
    IsEdited BOOLEAN NOT NULL,
    DateCreated DATETIME NOT NULL,
    PRIMARY KEY(Title),
    FOREIGN KEY(Title) REFERENCES SoundPlaylistsInfo(SoundTitle)
);

-- example of user creating a playlist called "liked"
CREATE TABLE Liked (
	SoundTitle VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY(SoundTitle)
);