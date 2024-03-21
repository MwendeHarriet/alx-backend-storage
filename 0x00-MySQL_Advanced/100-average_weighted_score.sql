-- creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
DETERMINISTIC
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight INT;
    DECLARE average_score FLOAT;

    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO total_weighted_score, total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    IF total_weight > 0 THEN
        SET average_score = total_weighted_score / total_weight;
    ELSE
        SET average_score = 0;
    END IF;

    UPDATE users
    SET average_score = average_score
    WHERE id = user_id;

END;
//

DELIMITER ;
