import { Sequelize } from "sequelize";

const sequelize = new Sequelize("gwc", "postgres", "root", {
  host: "localhost",
  port: 5432,
  dialect: "postgres",
  logging: false,
});

export default sequelize;
