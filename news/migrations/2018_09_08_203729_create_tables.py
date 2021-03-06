from orator.migrations import Migration


class CreateTables(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("users") as table:
            table.increments("id").unsigned()
            table.string("username", 32).unique()
            table.string("full_name", 64).nullable()
            table.string("email", 128).unique()
            table.boolean("email_verified").default(False)
            table.boolean("subscribed").default(False)
            table.boolean("email_public").default(False)
            table.string("password", 128)
            table.integer("reported").default(0)
            table.boolean("spammer").default(False)
            table.datetime("created_at")
            table.datetime("updated_at")
            table.string("preferred_sort", 10).default("trending")
            table.text("bio").nullable()
            table.text("url").nullable()
            table.text("profile_pic").nullable()
            table.integer("feed_subs").default(0)

            # preferences
            table.string("p_show_images", 1).default("y")
            table.integer("p_min_link_score").default(-3)

            # indexes
            table.index("username")
            table.index("email")
        with self.schema.create("feeds") as table:
            table.increments("id").unsigned()
            table.string("name", 64)
            table.string("slug", 80).unique()
            table.text("description").nullable()
            table.text("rules").nullable()
            table.text("img").nullable()
            table.integer("subscribers_count").default(0)
            table.string("default_sort", 12).default("trending")
            table.datetime("created_at")
            table.datetime("updated_at")
            table.string("lang", 12).default("en")
            table.boolean("over_18").default(False)
            table.string("logo", 128).nullable()
            table.boolean("reported").default(False)
            table.index("slug")
        with self.schema.create("links") as table:
            table.big_increments("id").unsigned()
            table.string("title", 128)
            table.string("slug", 150)
            table.text("text").nullable()
            table.text("image").nullable()
            table.text("url")
            table.integer("user_id").unsigned()
            table.datetime("created_at")
            table.datetime("updated_at")
            table.foreign("user_id").references("id").on("users")
            table.integer("feed_id").unsigned()
            table.foreign("feed_id").references("id").on("feeds").ondelete("cascade")
            table.integer("ups").default(0)
            table.integer("downs").default(0)
            table.integer("comments_count").default(0)
            table.boolean("archived").default(False)
            table.integer("reported").default(0)
            table.boolean("spam").default(False)
        with self.schema.create("reports") as table:
            table.increments("id").unsigned()
            table.string("reason", 16)
            table.text("comment")
            table.integer("feed_id").unsigned()
            table.foreign("feed_id").references("id").on("feeds").ondelete("cascade")
            table.integer("user_id").unsigned()
            table.foreign("user_id").references("id").on("users").ondelete("cascade")
            table.integer("reportable_id").unsigned()
            table.text("reportable_type")
            table.datetime("created_at")
            table.datetime("updated_at")
            table.index("user_id")
            table.index("feed_id")
        with self.schema.create("feeds_users") as table:
            table.integer("feed_id").unsigned()
            table.foreign("feed_id").references("id").on("feeds").ondelete("cascade")
            table.integer("user_id").unsigned()
            table.foreign("user_id").references("id").on("users").ondelete("cascade")
            table.index("feed_id")
            table.index("user_id")
            table.primary(["user_id", "feed_id"])
        with self.schema.create("feed_admins") as table:
            table.boolean("god").default(False)
            table.integer("user_id").unsigned()
            table.foreign("user_id").references("id").on("users").on_delete("cascade")
            table.integer("feed_id").unsigned()
            table.foreign("feed_id").references("id").on("feeds").on_delete("cascade")
            table.datetime("created_at")
            table.datetime("updated_at")
            table.primary(["user_id", "feed_id"])
        with self.schema.create("bans") as table:
            table.string("reason")
            table.integer("user_id").unsigned()
            table.foreign("user_id").references("id").on("users").on_delete("cascade")
            table.integer("feed_id").unsigned()
            table.foreign("feed_id").references("id").on("feeds").on_delete("cascade")
            table.datetime("created_at")
            table.datetime("updated_at")
            table.datetime("until")
            table.primary(["feed_id", "user_id"])
        with self.schema.create("comments") as table:
            table.big_increments("id").unsigned()
            table.big_integer("parent_id").unsigned().nullable()
            table.foreign("parent_id").references("id").on("comments").on_delete(
                "cascade"
            )
            table.text("text")
            table.integer("user_id").unsigned()
            table.foreign("user_id").references("id").on("users")
            table.integer("link_id").unsigned()
            table.foreign("link_id").references("id").on("links").on_delete("cascade")
            table.integer("reported").default(0)
            table.boolean("spam").default(False)
            table.integer("ups").default(0)
            table.integer("downs").default(0)
            table.datetime("created_at")
            table.datetime("updated_at")
        with self.schema.create("tokens") as table:
            table.string("id", 40)
        with self.schema.create("comment_votes") as table:
            table.integer("user_id").unsigned()
            table.foreign("user_id").references("id").on("users").on_delete("cascade")
            table.big_integer("comment_id").unsigned()
            table.foreign("comment_id").references("id").on("comments").on_delete(
                "cascade"
            )
            table.integer("vote_type")
            table.primary(["user_id", "comment_id"])
        with self.schema.create("link_votes") as table:
            table.integer("user_id").unsigned()
            table.foreign("user_id").references("id").on("users").on_delete("cascade")
            table.big_integer("link_id").unsigned()
            table.foreign("link_id").references("id").on("links").on_delete("cascade")
            table.integer("vote_type")
            table.primary(["user_id", "link_id"])

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("bans")
        self.schema.drop("comments")
        self.schema.drop("tokens")
        self.schema.drop("comment_votes")
        self.schema.drop("link_votes")
        self.schema.drop("feeds_users")
        self.schema.drop("reports")
        self.schema.drop("links")
        self.schema.drop("feeds")
        self.schema.drop("users")
