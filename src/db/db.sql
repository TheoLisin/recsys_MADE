CREATE DATABASE made_project;

USE made_project;

CREATE OR REPLACE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(64),
    pwdhash VARCHAR(64),
    INDEX users_ind(id)
);

-- [gid, orgid] is ignored
CREATE OR REPLACE TABLE authors (
    id INT NOT NULL PRIMARY KEY, -- users.id
    id_user INT,
    _id VARCHAR(64),
    avatar VARCHAR(128),
    sid VARCHAR(256),
    name VARCHAR(128),
    organisations VARCHAR(1024),
    orcid VARCHAR(128),
    position VARCHAR(32),
    email VARCHAR(128),
    bio VARCHAR(4096),
    homepage VARCHAR(256),
    INDEX author_ind(id),
    CONSTRAINT fk_user_author FOREIGN KEY (id_user) REFERENCES users(id)
);

-- [raw_zh, type, t, online_issn] is ignored
CREATE OR REPLACE TABLE venues (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    _id VARCHAR(64),
    raw_en VARCHAR(256),
    name VARCHAR(256),
    name_d VARCHAR(256),
    sid VARCHAR(256),
    publisher VARCHAR(256),
    issn VARCHAR(16),
    INDEX venue_ind(id)
);

-- [raw_zh, type, t, online_issn] is ignored
CREATE OR REPLACE TABLE articles (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_venue INT,
    _id VARCHAR(64),
    title VARCHAR(1024),
    pub_year VARCHAR(8),
    keywords VARCHAR(512),
    n_citation INT,
    page_start INT,
    page_end INT,
    volume VARCHAR(32),
    lang VARCHAR(2),
    issue VARCHAR(64),
    issn VARCHAR(512),
    isbn VARCHAR(64),
    doi VARCHAR(256),
    url_pdf VARCHAR(512),
    abstract TEXT,
    INDEX article_ind(id),
    CONSTRAINT fk_venue_article FOREIGN KEY (id_venue) REFERENCES venues(id)
);

CREATE OR REPLACE TABLE citations (
    id_where INT NOT NULL,
    id_what INT NOT NULL,
    PRIMARY KEY (id_where, id_what),
    CONSTRAINT fk_article_where FOREIGN KEY (id_where) REFERENCES articles(id),
    CONSTRAINT fk_article_what FOREIGN KEY (id_what) REFERENCES articles(id)
);

CREATE OR REPLACE TABLE authors_in_article (
    id_article INT NOT NULL,
    id_author INT NOT NULL,
    PRIMARY KEY (id_article, id_author),
    CONSTRAINT fk_article_article FOREIGN KEY (id_article) REFERENCES articles(id),
    CONSTRAINT fk_article_author FOREIGN KEY (id_author) REFERENCES authors(id)
);
