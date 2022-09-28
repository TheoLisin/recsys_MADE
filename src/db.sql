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
    sid VARCHAR(256),
    name VARCHAR(256),
    organisations VARCHAR(1024),
    orcid VARCHAR(128),
    position VARCHAR(256),
    email VARCHAR(128),
    bio VARCHAR(256),
    homepage VARCHAR(256),
    INDEX author_ind(id),
    CONSTRAINT fk_user_author FOREIGN KEY (id_user) REFERENCES users(id)
);

-- [raw_zh, type, t, online_issn] is ignored
CREATE OR REPLACE TABLE venues (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    raw_en VARCHAR(256),
    name_d VARCHAR(256),
    sid VARCHAR(128),
    publisher VARCHAR(128),
    issn VARCHAR(128),
    INDEX venue_ind(id)
);

-- [raw_zh, type, t, online_issn] is ignored
CREATE OR REPLACE TABLE articles (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_venue INT,
    title VARCHAR(256),
    pub_year VARCHAR(8),
    keywords VARCHAR(1024),
    n_citation INT,
    page_start INT,
    page_end INT,
    lang VARCHAR(16),
    issue VARCHAR(64),
    issn VARCHAR(64),
    isbn VARCHAR(64),
    doi VARCHAR(16),
    url_pdf VARCHAR(256),
    url VARCHAR(256),
    abstract VARCHAR(1024),
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
