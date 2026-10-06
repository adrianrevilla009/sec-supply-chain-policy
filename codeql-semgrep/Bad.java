import java.sql.*;

class Bad {
    String password = "hunter2";

    ResultSet find(Statement st, String id) throws SQLException {
        return st.executeQuery("select * from orders where id = " + id);
    }
}
