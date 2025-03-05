-- CREATE TABLE borrow (user_id int,
-- 					 book_id int,
--                      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
--                      FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE);                     








SELECT 
	br.user_id,
    u.f_name,
    u.l_name,
    u.book_count,
	br.book_id, 
    b.book_name, 
    b.writer, 
    b.pages_count, 
    b.print_count, 
    b.book_count
FROM borrow br
JOIN books b
ON br.book_id = b.book_id
JOIN users u
ON br.user_id = u.id;